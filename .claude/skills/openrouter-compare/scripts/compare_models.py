#!/usr/bin/env python3
"""Fan one prompt out to several OpenRouter models, compare, and export.

OpenRouter's `models` array is a *fallback* list: one request is served by the
first model that accepts it. To compare models you must send one request per
model. This script does that (concurrently), then writes:

    <out>/summary.md      human-readable comparison (tables, rankings, outputs)
    <out>/results.json    structured data: per-model records, metrics,
                          similarity matrix, chart-ready series
    <out>/figures.html    self-contained SVG bar charts + similarity heatmap
    <out>/raw/<model>.json  verbatim API response (or the list of SSE chunks)

Standard library only. Reads the API key from $OPENROUTER_API_KEY.

Examples:
    compare_models.py --config examples/skyscraper.json --out runs/skyscraper
    compare_models.py --model openai/gpt-5 --model anthropic/claude-opus-4.1 \\
        --prompt "Name the world's tallest skyscraper." --out runs/quick
    compare_models.py --config request.json --no-response-format --no-tools
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import html
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
CHAT_PATH = "/chat/completions"
# Keys in a chat/completions body that must not be forwarded per model.
STRIP_KEYS = {"models", "model", "route"}


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


# --------------------------------------------------------------------------- #
# Request construction
# --------------------------------------------------------------------------- #


def load_config(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    if not isinstance(cfg, dict):
        raise SystemExit(f"error: {path} must contain a JSON object (a chat/completions body)")
    return cfg


def resolve_models(cfg: dict[str, Any], cli_models: list[str]) -> list[str]:
    models: list[str] = []
    if cli_models:
        models = list(cli_models)
    elif isinstance(cfg.get("models"), list):
        models = [str(m) for m in cfg["models"]]
    elif cfg.get("model"):
        models = [str(cfg["model"])]
    # de-duplicate, preserve order
    seen: set[str] = set()
    out = []
    for m in models:
        if m not in seen:
            seen.add(m)
            out.append(m)
    if not out:
        raise SystemExit("error: no models given (use --model or a config with a `models` array)")
    return out


def resolve_messages(cfg: dict[str, Any], prompt: str | None, system: str | None) -> list[dict[str, Any]]:
    if prompt is not None:
        msgs: list[dict[str, Any]] = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        return msgs
    msgs = cfg.get("messages")
    if not isinstance(msgs, list) or not msgs:
        raise SystemExit("error: no messages (use --prompt or a config with `messages`)")
    if system:
        msgs = [m for m in msgs if m.get("role") != "system"]
        msgs.insert(0, {"role": "system", "content": system})
    return msgs


def build_body(cfg: dict[str, Any], model: str, messages: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    body = {k: v for k, v in cfg.items() if k not in STRIP_KEYS}
    body["model"] = model
    body["messages"] = messages
    body["stream"] = not args.no_stream
    if args.no_tools:
        body.pop("tools", None)
        body.pop("tool_choice", None)
    if args.no_response_format:
        body.pop("response_format", None)
    # Ask OpenRouter to attach token counts and cost to the response.
    usage = body.get("usage")
    if not isinstance(usage, dict):
        usage = {}
    usage.setdefault("include", True)
    body["usage"] = usage
    return body


def headers(api_key: str) -> dict[str, str]:
    h = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if os.environ.get("OPENROUTER_REFERER"):
        h["HTTP-Referer"] = os.environ["OPENROUTER_REFERER"]
    if os.environ.get("OPENROUTER_TITLE"):
        h["X-Title"] = os.environ["OPENROUTER_TITLE"]
    return h


# --------------------------------------------------------------------------- #
# Calling one model
# --------------------------------------------------------------------------- #


def new_record(model: str) -> dict[str, Any]:
    return {
        "model_requested": model,
        "model_served": None,
        "provider": None,
        "response_id": None,
        "ok": False,
        "error": None,
        "http_status": None,
        "content": "",
        "reasoning": "",
        "tool_calls": [],
        "finish_reason": None,
        "native_finish_reason": None,
        "usage": None,
        "parsed_json": None,
        "schema_valid": None,
        "schema_errors": [],
        "timing": {"start": None, "first_token": None, "end": None, "latency_s": None, "ttft_s": None},
        "raw_file": None,
    }


def merge_tool_call_delta(acc: list[dict[str, Any]], deltas: list[dict[str, Any]]) -> None:
    for d in deltas:
        idx = d.get("index", len(acc))
        while len(acc) <= idx:
            acc.append({"id": None, "type": "function", "function": {"name": "", "arguments": ""}})
        slot = acc[idx]
        if d.get("id"):
            slot["id"] = d["id"]
        if d.get("type"):
            slot["type"] = d["type"]
        fn = d.get("function") or {}
        if fn.get("name"):
            slot["function"]["name"] += fn["name"]
        if fn.get("arguments"):
            slot["function"]["arguments"] += fn["arguments"]


def apply_choice(rec: dict[str, Any], choice: dict[str, Any], delta_mode: bool) -> bool:
    """Fold one choice (delta or full message) into the record. Returns True if it carried output."""
    node = choice.get("delta") if delta_mode else choice.get("message")
    node = node or {}
    carried = False
    content = node.get("content")
    if isinstance(content, str) and content:
        rec["content"] += content
        carried = True
    elif isinstance(content, list):  # multimodal parts
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                rec["content"] += part.get("text", "")
                carried = True
    reasoning = node.get("reasoning") or node.get("reasoning_content")
    if isinstance(reasoning, str) and reasoning:
        rec["reasoning"] += reasoning
        carried = True
    tcs = node.get("tool_calls")
    if isinstance(tcs, list) and tcs:
        if delta_mode:
            merge_tool_call_delta(rec["tool_calls"], tcs)
        else:
            rec["tool_calls"] = tcs
        carried = True
    if choice.get("finish_reason"):
        rec["finish_reason"] = choice["finish_reason"]
    if choice.get("native_finish_reason"):
        rec["native_finish_reason"] = choice["native_finish_reason"]
    return carried


def apply_envelope(rec: dict[str, Any], obj: dict[str, Any]) -> None:
    if obj.get("id"):
        rec["response_id"] = obj["id"]
    if obj.get("model"):
        rec["model_served"] = obj["model"]
    if obj.get("provider"):
        rec["provider"] = obj["provider"]
    if isinstance(obj.get("usage"), dict):
        rec["usage"] = obj["usage"]


def read_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read().decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return exc.reason if isinstance(exc.reason, str) else str(exc)
    try:
        obj = json.loads(raw)
        err = obj.get("error") if isinstance(obj, dict) else None
        if isinstance(err, dict):
            msg = err.get("message") or json.dumps(err)
            meta = err.get("metadata")
            if isinstance(meta, dict) and meta.get("raw"):
                msg = f"{msg} | {meta['raw']}"
            return str(msg)
    except ValueError:
        pass
    return raw.strip()[:2000] or str(exc)


def call_model(model: str, body: dict[str, Any], base_url: str, api_key: str, timeout: float) -> tuple[dict[str, Any], Any]:
    """Return (record, raw). raw is the parsed JSON body or the list of SSE chunks."""
    rec = new_record(model)
    raw: Any = None
    req = urllib.request.Request(
        base_url.rstrip("/") + CHAT_PATH,
        data=json.dumps(body).encode("utf-8"),
        headers=headers(api_key),
        method="POST",
    )
    t0 = time.perf_counter()
    rec["timing"]["start"] = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            rec["http_status"] = resp.status
            ctype = resp.headers.get("Content-Type", "")
            if body.get("stream") and "text/event-stream" in ctype:
                chunks: list[Any] = []
                for line_b in resp:
                    line = line_b.decode("utf-8", "replace").rstrip("\r\n")
                    if not line or line.startswith(":"):
                        continue  # keep-alive comment, e.g. ": OPENROUTER PROCESSING"
                    if not line.startswith("data:"):
                        continue
                    payload = line[5:].strip()
                    if payload == "[DONE]":
                        break
                    try:
                        obj = json.loads(payload)
                    except ValueError:
                        chunks.append({"_unparsed": payload})
                        continue
                    chunks.append(obj)
                    if not isinstance(obj, dict):
                        continue
                    if isinstance(obj.get("error"), dict):
                        err = obj["error"]
                        rec["error"] = f"{err.get('code', '')} {err.get('message', json.dumps(err))}".strip()
                    apply_envelope(rec, obj)
                    for choice in obj.get("choices") or []:
                        if apply_choice(rec, choice, delta_mode=True) and rec["timing"]["first_token"] is None:
                            rec["timing"]["first_token"] = time.perf_counter() - t0
                raw = chunks
            else:
                text = resp.read().decode("utf-8", "replace")
                raw = json.loads(text)
                if isinstance(raw, dict):
                    if isinstance(raw.get("error"), dict):
                        err = raw["error"]
                        rec["error"] = f"{err.get('code', '')} {err.get('message', json.dumps(err))}".strip()
                    apply_envelope(rec, raw)
                    for choice in raw.get("choices") or []:
                        apply_choice(rec, choice, delta_mode=False)
                    rec["timing"]["first_token"] = time.perf_counter() - t0
    except urllib.error.HTTPError as exc:
        rec["http_status"] = exc.code
        rec["error"] = f"HTTP {exc.code}: {read_error_body(exc)}"
    except urllib.error.URLError as exc:
        rec["error"] = f"connection error: {exc.reason}"
    except TimeoutError:
        rec["error"] = f"timeout after {timeout:.0f}s"
    except Exception as exc:  # noqa: BLE001
        rec["error"] = f"{type(exc).__name__}: {exc}"
    t_end = time.perf_counter() - t0
    rec["timing"]["end"] = dt.datetime.now(dt.timezone.utc).isoformat()
    rec["timing"]["latency_s"] = round(t_end, 3)
    if rec["timing"]["first_token"] is not None:
        rec["timing"]["ttft_s"] = round(rec["timing"]["first_token"], 3)
    rec["timing"].pop("first_token", None)
    rec["ok"] = rec["error"] is None and bool(rec["content"] or rec["tool_calls"])
    if not rec["ok"] and rec["error"] is None:
        rec["error"] = "empty response (no content and no tool calls)"
    return rec, raw


# --------------------------------------------------------------------------- #
# Structured-output validation (small JSON-Schema subset)
# --------------------------------------------------------------------------- #

_JSON_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def validate_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    typ = schema.get("type")
    if typ:
        types = typ if isinstance(typ, list) else [typ]
        ok = False
        for t in types:
            py = _JSON_TYPES.get(t)
            if py is None:
                continue
            if isinstance(instance, bool) and t in ("integer", "number"):
                continue
            if isinstance(instance, py):
                ok = True
                break
        if not ok:
            errors.append(f"{path}: expected type {typ}, got {type(instance).__name__}")
            return errors
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property '{key}'")
        for key, val in instance.items():
            if key in props:
                errors.extend(validate_schema(val, props[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: additional property '{key}' not allowed")
    if isinstance(instance, list) and isinstance(schema.get("items"), dict):
        for i, item in enumerate(instance):
            errors.extend(validate_schema(item, schema["items"], f"{path}[{i}]"))
    return errors


def extract_json(text: str) -> Any:
    """Parse JSON from a response, tolerating a ```json fence around it."""
    s = text.strip()
    if not s:
        raise ValueError("empty")
    try:
        return json.loads(s)
    except ValueError:
        pass
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.S)
    if m:
        return json.loads(m.group(1))
    start = min([i for i in (s.find("{"), s.find("[")) if i >= 0], default=-1)
    if start >= 0:
        return json.loads(s[start:])
    raise ValueError("no JSON found")


def apply_structured_checks(rec: dict[str, Any], response_format: dict[str, Any] | None) -> None:
    if not rec["ok"] or not response_format:
        return
    fmt_type = response_format.get("type")
    if fmt_type not in ("json_object", "json_schema"):
        return
    try:
        rec["parsed_json"] = extract_json(rec["content"])
    except ValueError as exc:
        rec["schema_valid"] = False
        rec["schema_errors"] = [f"output is not JSON: {exc}"]
        return
    if fmt_type == "json_schema":
        schema = (response_format.get("json_schema") or {}).get("schema") or {}
        errs = validate_schema(rec["parsed_json"], schema)
        rec["schema_valid"] = not errs
        rec["schema_errors"] = errs
    else:
        rec["schema_valid"] = True


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #

_WORD_RE = re.compile(r"[a-z0-9']+")


def word_set(text: str) -> set[str]:
    return {w for w in _WORD_RE.findall(text.lower()) if len(w) > 2}


def jaccard(a: set[str], b: set[str]) -> float | None:
    if not a and not b:
        return None
    return len(a & b) / len(a | b)


def output_text(rec: dict[str, Any]) -> str:
    if rec["content"]:
        return rec["content"]
    if rec["tool_calls"]:
        return " ".join(
            f"{tc.get('function', {}).get('name', '')} {tc.get('function', {}).get('arguments', '')}" for tc in rec["tool_calls"]
        )
    return ""


def per_model_metrics(rec: dict[str, Any]) -> dict[str, Any]:
    usage = rec.get("usage") or {}
    text = output_text(rec)
    completion = usage.get("completion_tokens")
    ttft = rec["timing"].get("ttft_s")
    lat = rec["timing"].get("latency_s")
    tps = None
    if completion and lat is not None and ttft is not None and lat - ttft > 0.05:
        tps = round(completion / (lat - ttft), 1)
    return {
        "model": rec["model_requested"],
        "model_served": rec["model_served"],
        "provider": rec["provider"],
        "ok": rec["ok"],
        "latency_s": lat,
        "ttft_s": ttft,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": completion,
        "total_tokens": usage.get("total_tokens"),
        "reasoning_tokens": ((usage.get("completion_tokens_details") or {}).get("reasoning_tokens")),
        "cost_usd": usage.get("cost"),
        "tokens_per_s": tps,
        "output_chars": len(text),
        "output_words": len(_WORD_RE.findall(text.lower())),
        "tool_calls": len(rec["tool_calls"]),
        "finish_reason": rec["finish_reason"],
        "schema_valid": rec["schema_valid"],
        "error": rec["error"],
    }


def similarity_matrix(records: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [r["model_requested"] for r in records]
    sets = [word_set(output_text(r)) if r["ok"] else set() for r in records]
    n = len(records)
    matrix: list[list[float | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if not records[i]["ok"] or not records[j]["ok"]:
                continue
            matrix[i][j] = 1.0 if i == j else round(jaccard(sets[i], sets[j]) or 0.0, 3)
    centrality = []
    for i in range(n):
        vals = [matrix[i][j] for j in range(n) if j != i and matrix[i][j] is not None]
        centrality.append(round(sum(vals) / len(vals), 3) if vals else None)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] is not None:
                pairs.append({"a": labels[i], "b": labels[j], "jaccard": matrix[i][j]})
    pairs.sort(key=lambda p: p["jaccard"], reverse=True)
    return {"metric": "jaccard_word_sets", "labels": labels, "matrix": matrix, "mean_similarity": centrality, "pairs": pairs}


def field_agreement(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    dicts = [(r["model_requested"], r["parsed_json"]) for r in records if isinstance(r.get("parsed_json"), dict)]
    if len(dicts) < 2:
        return None
    keys: list[str] = []
    for _, d in dicts:
        for k in d:
            if k not in keys:
                keys.append(k)
    out: dict[str, Any] = {}
    for k in keys:
        groups: dict[str, list[str]] = {}
        for model, d in dicts:
            if k in d:
                norm = json.dumps(d[k], sort_keys=True, ensure_ascii=False)
                groups.setdefault(norm, []).append(model)
        ranked = sorted(groups.items(), key=lambda kv: len(kv[1]), reverse=True)
        present = sum(len(v) for v in groups.values())
        out[k] = {
            "models_with_field": present,
            "distinct_values": len(groups),
            "majority_value": json.loads(ranked[0][0]) if ranked else None,
            "majority_share": round(len(ranked[0][1]) / present, 3) if ranked else None,
            "values": [{"value": json.loads(v), "models": ms} for v, ms in ranked],
        }
    return out


def rankings(metrics: list[dict[str, Any]], sim: dict[str, Any]) -> dict[str, Any]:
    ok = [m for m in metrics if m["ok"]]

    def best(key: str, reverse: bool = False) -> dict[str, Any] | None:
        cands = [m for m in ok if isinstance(m.get(key), (int, float))]
        if not cands:
            return None
        m = sorted(cands, key=lambda x: x[key], reverse=reverse)[0]
        return {"model": m["model"], "value": m[key]}

    central = None
    cvals = [(lbl, v) for lbl, v in zip(sim["labels"], sim["mean_similarity"]) if v is not None]
    if cvals:
        lbl, v = max(cvals, key=lambda x: x[1])
        central = {"model": lbl, "value": v}
    outlier = None
    if len(cvals) > 1:
        lbl, v = min(cvals, key=lambda x: x[1])
        outlier = {"model": lbl, "value": v}
    return {
        "fastest_total": best("latency_s"),
        "fastest_first_token": best("ttft_s"),
        "cheapest": best("cost_usd"),
        "fewest_completion_tokens": best("completion_tokens"),
        "most_completion_tokens": best("completion_tokens", reverse=True),
        "highest_throughput": best("tokens_per_s", reverse=True),
        "longest_output_words": best("output_words", reverse=True),
        "shortest_output_words": best("output_words"),
        "most_consensual": central,
        "most_divergent": outlier,
    }


def chart_series(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [m["model"] for m in metrics]

    def series(key: str, unit: str, title: str) -> dict[str, Any]:
        # Failed models carry no comparable measurement; they plot as n/a.
        return {"title": title, "unit": unit, "labels": labels, "values": [m.get(key) if m["ok"] else None for m in metrics]}

    return {
        "latency_s": series("latency_s", "s", "Total latency"),
        "ttft_s": series("ttft_s", "s", "Time to first token"),
        "completion_tokens": series("completion_tokens", "tokens", "Completion tokens"),
        "prompt_tokens": series("prompt_tokens", "tokens", "Prompt tokens"),
        "cost_usd": series("cost_usd", "USD", "Cost"),
        "tokens_per_s": series("tokens_per_s", "tok/s", "Decode throughput"),
        "output_words": series("output_words", "words", "Output length"),
    }


# --------------------------------------------------------------------------- #
# Exports
# --------------------------------------------------------------------------- #


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s).strip("_") or "model"


def fmt(v: Any, digits: int = 2) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        if v != 0 and abs(v) < 0.01:
            return f"{v:.3g}"
        return f"{v:.{digits}f}"
    return str(v)


def md_escape(s: Any) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def render_messages_md(messages: list[dict[str, Any]]) -> str:
    parts = []
    for m in messages:
        content = m.get("content")
        if not isinstance(content, str):
            content = json.dumps(content, ensure_ascii=False, indent=2)
        parts.append(f"**{m.get('role', '?')}**\n\n```text\n{content}\n```")
    return "\n\n".join(parts)


def write_summary_md(path: str, run: dict[str, Any], records: list[dict[str, Any]], metrics: list[dict[str, Any]], sim: dict[str, Any], agree: dict[str, Any] | None, ranks: dict[str, Any]) -> None:
    ok_n = sum(1 for r in records if r["ok"])
    L: list[str] = []
    L.append(f"# OpenRouter multi-model comparison: {run['title']}")
    L.append("")
    L.append(f"- Run started: {run['started_at']}")
    L.append(f"- Endpoint: `{run['base_url']}{CHAT_PATH}`")
    L.append(f"- Models requested: {len(records)}; succeeded: {ok_n}; failed: {len(records) - ok_n}")
    L.append(f"- Streaming: {'on' if run['stream'] else 'off'}; per-request timeout: {run['timeout_s']:.0f} s; concurrency: {run['concurrency']}")
    opts = run["request_options"]
    if opts.get("tools"):
        L.append(f"- Tools offered: {', '.join(f'`{t}`' for t in opts['tools'])}")
    if opts.get("response_format"):
        L.append(f"- Response format: `{opts['response_format']}`")
    extra = {k: v for k, v in opts.items() if k not in ("tools", "response_format")}
    if extra:
        L.append(f"- Other options: `{json.dumps(extra, ensure_ascii=False)}`")
    L.append("")
    L.append("## Prompt")
    L.append("")
    L.append(render_messages_md(run["messages"]))
    L.append("")
    L.append("## Comparison table")
    L.append("")
    has_schema = any(m["schema_valid"] is not None for m in metrics)
    cols = ["#", "Model", "Served as", "Provider", "Status", "Latency (s)", "TTFT (s)", "Prompt tok", "Completion tok", "Tok/s", "Cost (USD)", "Words", "Tool calls", "Finish"]
    if has_schema:
        cols.append("Schema valid")
    L.append("| " + " | ".join(cols) + " |")
    L.append("|" + "|".join(["---"] * len(cols)) + "|")
    for i, m in enumerate(metrics, 1):
        status = "ok" if m["ok"] else "FAIL"
        row = [
            str(i), f"`{m['model']}`", f"`{m['model_served']}`" if m["model_served"] else "n/a", m["provider"] or "n/a", status,
            fmt(m["latency_s"]), fmt(m["ttft_s"]), fmt(m["prompt_tokens"]), fmt(m["completion_tokens"]), fmt(m["tokens_per_s"], 1),
            fmt(m["cost_usd"], 5), fmt(m["output_words"]), fmt(m["tool_calls"]), m["finish_reason"] or "n/a",
        ]
        if has_schema:
            row.append(fmt(m["schema_valid"]))
        L.append("| " + " | ".join(md_escape(c) for c in row) + " |")
    L.append("")
    L.append("## Rankings")
    L.append("")
    names = {
        "fastest_total": "Fastest (total latency)", "fastest_first_token": "Fastest first token", "cheapest": "Cheapest",
        "fewest_completion_tokens": "Fewest completion tokens", "most_completion_tokens": "Most completion tokens",
        "highest_throughput": "Highest decode throughput", "longest_output_words": "Longest output", "shortest_output_words": "Shortest output",
        "most_consensual": "Most consensual (highest mean Jaccard to others)", "most_divergent": "Most divergent (lowest mean Jaccard to others)",
    }
    for k, label in names.items():
        v = ranks.get(k)
        if v:
            L.append(f"- {label}: `{v['model']}` ({fmt(v['value'], 3)})")
    L.append("")
    L.append("## Pairwise similarity (Jaccard over word sets, words longer than two characters)")
    L.append("")
    labels = sim["labels"]
    L.append("| | " + " | ".join(f"`{md_escape(l)}`" for l in labels) + " | mean |")
    L.append("|---|" + "|".join(["---"] * len(labels)) + "|---|")
    for i, l in enumerate(labels):
        cells = [fmt(sim["matrix"][i][j], 2) for j in range(len(labels))]
        L.append(f"| `{md_escape(l)}` | " + " | ".join(cells) + f" | {fmt(sim['mean_similarity'][i], 2)} |")
    L.append("")
    if sim["pairs"]:
        hi, lo = sim["pairs"][0], sim["pairs"][-1]
        L.append(f"Most similar pair: `{hi['a']}` and `{hi['b']}` ({hi['jaccard']:.2f}). Least similar pair: `{lo['a']}` and `{lo['b']}` ({lo['jaccard']:.2f}).")
        L.append("")
    if agree:
        L.append("## Field agreement (structured output)")
        L.append("")
        L.append("| Field | Models with field | Distinct values | Majority value | Majority share |")
        L.append("|---|---|---|---|---|")
        for k, v in agree.items():
            L.append(f"| `{md_escape(k)}` | {v['models_with_field']} | {v['distinct_values']} | `{md_escape(json.dumps(v['majority_value'], ensure_ascii=False))[:80]}` | {fmt(v['majority_share'], 2)} |")
        L.append("")
        for k, v in agree.items():
            if v["distinct_values"] > 1:
                L.append(f"<details><summary>Values for <code>{html.escape(k)}</code></summary>")
                L.append("")
                for entry in v["values"]:
                    L.append(f"- `{md_escape(json.dumps(entry['value'], ensure_ascii=False))}` from {', '.join(f'`{m}`' for m in entry['models'])}")
                L.append("")
                L.append("</details>")
                L.append("")
    L.append("## Outputs")
    L.append("")
    for r, m in zip(records, metrics):
        L.append(f"### `{r['model_requested']}`")
        L.append("")
        if not r["ok"]:
            L.append(f"**Failed.** {r['error']}")
            L.append("")
            continue
        meta = f"served as `{r['model_served'] or 'n/a'}` via {r['provider'] or 'n/a'}; finish `{r['finish_reason']}`; {fmt(m['latency_s'])} s; {fmt(m['completion_tokens'])} completion tokens"
        if m["cost_usd"] is not None:
            meta += f"; ${fmt(m['cost_usd'], 5)}"
        L.append(meta)
        L.append("")
        if r["reasoning"]:
            L.append("<details><summary>Reasoning</summary>")
            L.append("")
            L.append("```text")
            L.append(r["reasoning"].replace("```", "` ` `"))
            L.append("```")
            L.append("")
            L.append("</details>")
            L.append("")
        if r["content"]:
            lang = "json" if r["parsed_json"] is not None else "text"
            L.append(f"```{lang}")
            L.append(r["content"].replace("```", "` ` `"))
            L.append("```")
            L.append("")
        if r["tool_calls"]:
            L.append("Tool calls:")
            L.append("")
            for tc in r["tool_calls"]:
                fn = tc.get("function", {})
                L.append(f"- `{fn.get('name')}` with arguments `{md_escape(fn.get('arguments'))}`")
            L.append("")
        if r["schema_valid"] is False:
            L.append("Schema violations:")
            L.append("")
            for e in r["schema_errors"]:
                L.append(f"- {e}")
            L.append("")
    failed = [r for r in records if not r["ok"]]
    if failed:
        L.append("## Failures")
        L.append("")
        for r in failed:
            L.append(f"- `{r['model_requested']}` (HTTP {r['http_status'] or 'n/a'}): {r['error']}")
        L.append("")
    L.append("---")
    L.append("Files: `results.json` (structured data and chart series), `figures.html` (SVG charts), `raw/` (verbatim responses).")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


# ----- figures.html (inline SVG, no dependencies) -------------------------- #

CSS = """
.viz-root{color-scheme:light;--surface-1:#fcfcfb;--page:#f9f9f7;--text-primary:#0b0b0b;--text-secondary:#52514e;--muted:#898781;--grid:#e1e0d9;--axis:#c3c2b7;--series-1:#2a78d6;--seq-100:#cde2fb;--seq-700:#0d366b;--border:rgba(11,11,11,.10)}
@media (prefers-color-scheme: dark){:root:where(:not([data-theme="light"])) .viz-root{color-scheme:dark;--surface-1:#1a1a19;--page:#0d0d0d;--text-primary:#fff;--text-secondary:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--axis:#383835;--series-1:#3987e5;--seq-100:#184f95;--seq-700:#cde2fb;--border:rgba(255,255,255,.10)}}
:root[data-theme="dark"] .viz-root{color-scheme:dark;--surface-1:#1a1a19;--page:#0d0d0d;--text-primary:#fff;--text-secondary:#c3c2b7;--muted:#898781;--grid:#2c2c2a;--axis:#383835;--series-1:#3987e5;--seq-100:#184f95;--seq-700:#cde2fb;--border:rgba(255,255,255,.10)}
.viz-root{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--page);color:var(--text-primary);margin:0;padding:24px;min-height:100vh}
.viz-root h1{font-size:20px;font-weight:600;margin:0 0 4px}
.viz-root p.sub{color:var(--text-secondary);margin:0 0 20px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px}
.card{background:var(--surface-1);border:1px solid var(--border);border-radius:8px;padding:16px;overflow-x:auto}
.card h2{font-size:14px;font-weight:600;margin:0 0 2px}
.card .unit{color:var(--muted);font-size:12px;margin:0 0 8px}
.bar{fill:var(--series-1)}
.bar:hover{opacity:.85}
.lbl{fill:var(--text-secondary);font-size:12px}
.val{fill:var(--text-primary);font-size:12px;font-variant-numeric:tabular-nums}
.tick{fill:var(--muted);font-size:11px;font-variant-numeric:tabular-nums}
.gridline{stroke:var(--grid);stroke-width:1}
.baseline{stroke:var(--axis);stroke-width:1}
.na{fill:var(--muted);font-size:12px;font-style:italic}
.cell text{font-size:11px;font-variant-numeric:tabular-nums}
table.data{border-collapse:collapse;font-size:12px;width:100%}
table.data th,table.data td{border-bottom:1px solid var(--grid);padding:4px 8px;text-align:right;font-variant-numeric:tabular-nums}
table.data th:first-child,table.data td:first-child{text-align:left}
"""


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _lerp_hex(a: str, b: str, t: float) -> str:
    ra, ga, ba = _hex_to_rgb(a)
    rb, gb, bb = _hex_to_rgb(b)
    return "#%02x%02x%02x" % (round(ra + (rb - ra) * t), round(ga + (gb - ga) * t), round(ba + (bb - ba) * t))


def _nice_max(v: float) -> float:
    if v <= 0:
        return 1.0
    exp = math.floor(math.log10(v))
    frac = v / (10 ** exp)
    nice = 1 if frac <= 1 else 2 if frac <= 2 else 5 if frac <= 5 else 10
    return nice * (10 ** exp)


def bar_chart_svg(series: dict[str, Any]) -> str:
    labels, values = series["labels"], series["values"]
    nums = [v for v in values if isinstance(v, (int, float))]
    if not nums:
        return f"<p class='na'>No data for {html.escape(series['title'])}.</p>"
    vmax = _nice_max(max(nums))
    label_w, val_w, bar_h, gap, top, left_pad = 220, 70, 18, 8, 22, 8
    plot_w = 320
    width = label_w + plot_w + val_w + left_pad
    height = top + len(labels) * (bar_h + gap) + 14
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(series["title"])} by model" style="max-width:{width}px;height:auto">']
    ticks = 4
    for k in range(ticks + 1):
        x = label_w + plot_w * k / ticks
        tv = vmax * k / ticks
        parts.append(f'<line class="gridline" x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{height - 14}"/>')
        parts.append(f'<text class="tick" x="{x:.1f}" y="{top - 8}" text-anchor="middle">{fmt(tv, 2 if vmax < 10 else 0)}</text>')
    parts.append(f'<line class="baseline" x1="{label_w}" y1="{top - 4}" x2="{label_w}" y2="{height - 14}"/>')
    for i, (lbl, v) in enumerate(zip(labels, values)):
        y = top + i * (bar_h + gap)
        short = lbl if len(lbl) <= 30 else lbl[:29] + "…"
        parts.append(f'<text class="lbl" x="{label_w - 8}" y="{y + bar_h * 0.72:.1f}" text-anchor="end">{html.escape(short)}</text>')
        if isinstance(v, (int, float)):
            w = plot_w * (v / vmax) if vmax else 0
            w = max(w, 2)
            title = f"{lbl}: {fmt(v, 4)} {series['unit']}"
            parts.append(f'<g><title>{html.escape(title)}</title><path class="bar" d="M{label_w},{y} h{w - 4:.1f} a4,4 0 0 1 4,4 v{bar_h - 8} a4,4 0 0 1 -4,4 h-{w - 4:.1f} z"/></g>')
            parts.append(f'<text class="val" x="{label_w + w + 6:.1f}" y="{y + bar_h * 0.72:.1f}">{fmt(v, 3 if vmax < 10 else 0)}</text>')
        else:
            parts.append(f'<text class="na" x="{label_w + 6}" y="{y + bar_h * 0.72:.1f}">n/a</text>')
    parts.append("</svg>")
    return "".join(parts)


def heatmap_svg(sim: dict[str, Any]) -> str:
    labels, matrix = sim["labels"], sim["matrix"]
    n = len(labels)
    cell, label_w, top = 44, 220, 130
    width = label_w + n * cell + 8
    height = top + n * cell + 8
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="Pairwise output similarity" style="max-width:{width}px;height:auto">']
    for j, lbl in enumerate(labels):
        short = lbl if len(lbl) <= 24 else lbl[:23] + "…"
        x = label_w + j * cell + cell / 2
        parts.append(f'<text class="lbl" transform="translate({x:.1f},{top - 6}) rotate(-60)" text-anchor="start">{html.escape(short)}</text>')
    for i, lbl in enumerate(labels):
        short = lbl if len(lbl) <= 30 else lbl[:29] + "…"
        y = top + i * cell
        parts.append(f'<text class="lbl" x="{label_w - 8}" y="{y + cell * 0.6:.1f}" text-anchor="end">{html.escape(short)}</text>')
        for j in range(n):
            v = matrix[i][j]
            x = label_w + j * cell
            if v is None:
                parts.append(f'<rect x="{x + 1}" y="{y + 1}" width="{cell - 2}" height="{cell - 2}" rx="3" fill="none" stroke="var(--grid)"/>')
                continue
            color = _lerp_hex("#cde2fb", "#0d366b", v)
            ink = "#ffffff" if v > 0.55 else "#0b0b0b"
            parts.append(f'<g class="cell"><title>{html.escape(labels[i])} vs {html.escape(labels[j])}: {v:.2f}</title>'
                         f'<rect x="{x + 1}" y="{y + 1}" width="{cell - 2}" height="{cell - 2}" rx="3" fill="{color}"/>'
                         f'<text x="{x + cell / 2:.1f}" y="{y + cell * 0.6:.1f}" text-anchor="middle" fill="{ink}">{v:.2f}</text></g>')
    parts.append("</svg>")
    return "".join(parts)


def write_figures_html(path: str, run: dict[str, Any], metrics: list[dict[str, Any]], charts: dict[str, Any], sim: dict[str, Any]) -> None:
    ok_n = sum(1 for m in metrics if m["ok"])
    cards = []
    for key in ("latency_s", "ttft_s", "completion_tokens", "tokens_per_s", "cost_usd", "output_words"):
        s = charts[key]
        cards.append(f"<div class='card'><h2>{html.escape(s['title'])}</h2><p class='unit'>{html.escape(s['unit'])}, one bar per model; failed models show n/a</p>{bar_chart_svg(s)}</div>")
    cards.append(f"<div class='card' style='grid-column:1/-1'><h2>Pairwise output similarity</h2><p class='unit'>Jaccard index over word sets; darker is more similar</p>{heatmap_svg(sim)}</div>")
    rows = []
    for m in metrics:
        rows.append("<tr>" + "".join(f"<td>{html.escape(fmt(m[k], 3))}</td>" for k in ("model", "provider", "latency_s", "ttft_s", "prompt_tokens", "completion_tokens", "tokens_per_s", "cost_usd", "output_words", "finish_reason")) + "</tr>")
    table = ("<div class='card' style='grid-column:1/-1'><h2>Data table</h2><p class='unit'>Same values as the charts</p><table class='data'><thead><tr>"
             + "".join(f"<th>{h}</th>" for h in ("Model", "Provider", "Latency s", "TTFT s", "Prompt tok", "Completion tok", "Tok/s", "Cost USD", "Words", "Finish"))
             + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>")
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(run['title'])} model comparison</title><style>{CSS}</style></head>
<body class="viz-root">
<h1>{html.escape(run['title'])}</h1>
<p class="sub">{len(metrics)} models requested, {ok_n} succeeded. Run started {html.escape(run['started_at'])}. Source: results.json.</p>
<div class="grid">{''.join(cards)}{table}</div>
</body></html>
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", help="JSON file: an OpenRouter chat/completions body (models, messages, tools, response_format, ...)")
    p.add_argument("--model", action="append", default=[], help="Model ID to include (repeatable; overrides the config's models)")
    p.add_argument("--prompt", help="User prompt (overrides the config's messages)")
    p.add_argument("--system", help="System prompt (replaces any system message)")
    p.add_argument("--out", default=None, help="Output directory (default: runs/<timestamp>)")
    p.add_argument("--title", default=None, help="Title used in summary.md and figures.html")
    p.add_argument("--base-url", default=os.environ.get("OPENROUTER_BASE_URL", DEFAULT_BASE_URL), help="API base URL (default: %(default)s)")
    p.add_argument("--api-key", default=None, help="API key (default: $OPENROUTER_API_KEY)")
    p.add_argument("--timeout", type=float, default=180.0, help="Per-request timeout in seconds (default: 180)")
    p.add_argument("--concurrency", type=int, default=8, help="Max simultaneous requests (default: 8)")
    p.add_argument("--no-stream", action="store_true", help="Disable SSE streaming (no time-to-first-token then)")
    p.add_argument("--no-tools", action="store_true", help="Drop `tools`/`tool_choice` from the request")
    p.add_argument("--no-response-format", action="store_true", help="Drop `response_format` from the request")
    p.add_argument("--quiet", action="store_true", help="Suppress per-model progress on stderr")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    cfg = load_config(args.config)
    models = resolve_models(cfg, args.model)
    messages = resolve_messages(cfg, args.prompt, args.system)
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        eprint("error: set OPENROUTER_API_KEY (or pass --api-key)")
        return 2

    started = dt.datetime.now(dt.timezone.utc)
    out_dir = args.out or os.path.join("runs", started.strftime("%Y%m%dT%H%M%SZ"))
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)

    bodies = {m: build_body(cfg, m, messages, args) for m in models}
    template = dict(next(iter(bodies.values())))
    template.pop("model", None)
    template.pop("messages", None)
    request_options: dict[str, Any] = {}
    if template.get("tools"):
        request_options["tools"] = [t.get("function", {}).get("name", t.get("type")) for t in template["tools"]]
    if template.get("response_format"):
        rf = template["response_format"]
        request_options["response_format"] = rf.get("type") + (":" + rf["json_schema"]["name"] if rf.get("type") == "json_schema" and rf.get("json_schema", {}).get("name") else "")
    for k in ("temperature", "top_p", "max_tokens", "reasoning", "provider", "seed", "tool_choice"):
        if k in template:
            request_options[k] = template[k]

    user_text = next((m.get("content") for m in reversed(messages) if m.get("role") == "user" and isinstance(m.get("content"), str)), "")
    title = args.title or (user_text[:60] + ("…" if len(user_text) > 60 else "")) or "untitled"
    run = {
        "title": title,
        "started_at": started.isoformat(),
        "base_url": args.base_url.rstrip("/"),
        "stream": not args.no_stream,
        "timeout_s": args.timeout,
        "concurrency": max(1, min(args.concurrency, len(models))),
        "models_requested": models,
        "messages": messages,
        "request_options": request_options,
        "request_template": template,
        "config_file": args.config,
    }

    if not args.quiet:
        eprint(f"Querying {len(models)} models via {run['base_url']}{CHAT_PATH} (concurrency {run['concurrency']}) ...")
    results: dict[str, tuple[dict[str, Any], Any]] = {}
    with cf.ThreadPoolExecutor(max_workers=run["concurrency"]) as pool:
        futs = {pool.submit(call_model, m, bodies[m], args.base_url, api_key, args.timeout): m for m in models}
        for fut in cf.as_completed(futs):
            m = futs[fut]
            rec, raw = fut.result()
            results[m] = (rec, raw)
            if not args.quiet:
                status = "ok" if rec["ok"] else f"FAIL ({rec['error']})"
                eprint(f"  {m}: {status} in {rec['timing']['latency_s']} s")

    records: list[dict[str, Any]] = []
    for m in models:
        rec, raw = results[m]
        raw_path = os.path.join(raw_dir, slug(m) + ".json")
        with open(raw_path, "w", encoding="utf-8") as fh:
            json.dump(raw, fh, indent=2, ensure_ascii=False)
        rec["raw_file"] = os.path.relpath(raw_path, out_dir)
        apply_structured_checks(rec, None if args.no_response_format else cfg.get("response_format"))
        records.append(rec)

    metrics = [per_model_metrics(r) for r in records]
    sim = similarity_matrix(records)
    agree = field_agreement(records)
    ranks = rankings(metrics, sim)
    charts = chart_series(metrics)

    results_json = {
        "schema_version": 1,
        "run": run,
        "results": records,
        "metrics": {"per_model": metrics, "rankings": ranks, "similarity": sim, "field_agreement": agree},
        "chart_data": charts,
    }
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results_json, fh, indent=2, ensure_ascii=False)
    write_summary_md(os.path.join(out_dir, "summary.md"), run, records, metrics, sim, agree, ranks)
    write_figures_html(os.path.join(out_dir, "figures.html"), run, metrics, charts, sim)

    ok_n = sum(1 for r in records if r["ok"])
    print(f"{ok_n}/{len(records)} models succeeded. Wrote {out_dir}/summary.md, results.json, figures.html, raw/")
    if not args.quiet:
        for m in metrics:
            flag = "ok  " if m["ok"] else "FAIL"
            eprint(f"  {flag} {m['model']:<45} {fmt(m['latency_s']):>7} s  {fmt(m['completion_tokens']):>6} tok  ${fmt(m['cost_usd'], 5)}")
    return 0 if ok_n else 1


if __name__ == "__main__":
    sys.exit(main())
