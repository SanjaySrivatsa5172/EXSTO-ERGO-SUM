#!/usr/bin/env python3
"""Offline self-test: runs compare_models.py against a local mock OpenRouter.

The mock serves POST /api/v1/chat/completions with per-model behaviour chosen
by the model ID, so every code path is exercised without an API key:

    contains "json"     -> streams valid calendar_event JSON
    contains "tool"     -> streams a get_weather tool call (no content)
    contains "badjson"  -> streams JSON that violates the schema
    contains "reason"   -> streams reasoning deltas before content
    contains "missing"  -> HTTP 404 "No endpoints found"
    contains "slow"     -> sleeps past the client timeout
    contains "midstream"-> streams a chunk, then an in-stream error object
    anything else       -> streams plain prose (or returns JSON when stream=false)

Usage:
    python3 selftest.py            # run all checks, exit 0 on success
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import compare_models  # noqa: E402

PROSE = {
    "alpha": "I would name it Aetherion Spire, a tower reaching toward the aether above the clouds.",
    "beta": "The tower would be called Aetherion Spire because it reaches toward the clouds and the sky.",
    "gamma": "Call it Meridian One. Short names age well on skylines.",
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # silence
        pass

    def _chunk(self, model: str, delta: dict, finish=None, usage=None, extra=None) -> bytes:
        obj = {"id": "gen-test", "provider": "MockProvider", "model": model + "-served", "object": "chat.completion.chunk",
               "created": int(time.time()), "choices": [{"index": 0, "delta": delta, "finish_reason": finish, "native_finish_reason": finish}]}
        if usage:
            obj["usage"] = usage
        if extra:
            obj.update(extra)
        return f"data: {json.dumps(obj)}\n\n".encode()

    def do_POST(self):
        if self.path != "/api/v1/chat/completions":
            self.send_error(404)
            return
        if self.headers.get("Authorization") != "Bearer test-key":
            self._json(401, {"error": {"code": 401, "message": "No auth credentials found"}})
            return
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        model = body["model"]
        assert "models" not in body, "fan-out must not forward the models array"
        assert body.get("usage", {}).get("include") is True
        if "missing" in model:
            self._json(404, {"error": {"code": 404, "message": f"No endpoints found for {model}."}})
            return
        if "slow" in model:
            time.sleep(3)
            self._json(200, {"choices": []})
            return
        usage = {"prompt_tokens": 40, "completion_tokens": 20, "total_tokens": 60, "cost": 0.00042}
        if "json" in model:
            text = json.dumps({"name": "Aetherion Spire", "date": "2031-01-01", "participants": ["architect"]})
        elif "badjson" in model:
            text = json.dumps({"name": "Meridian One", "extra": 1})
        else:
            text = PROSE.get(model.split("/")[-1], PROSE["alpha"])
        if "badjson" in model:
            text = json.dumps({"name": "Meridian One", "extra": 1})
        if not body.get("stream"):
            msg = {"role": "assistant", "content": text}
            self._json(200, {"id": "gen-test", "provider": "MockProvider", "model": model + "-served",
                             "choices": [{"index": 0, "message": msg, "finish_reason": "stop"}], "usage": usage})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        w = self.wfile
        w.write(b": OPENROUTER PROCESSING\n\n")
        w.flush()
        time.sleep(0.05)
        if "tool" in model:
            w.write(self._chunk(model, {"role": "assistant", "tool_calls": [{"index": 0, "id": "call_1", "type": "function", "function": {"name": "get_weather", "arguments": ""}}]}))
            w.write(self._chunk(model, {"tool_calls": [{"index": 0, "function": {"arguments": '{"location": '}}]}))
            w.write(self._chunk(model, {"tool_calls": [{"index": 0, "function": {"arguments": '"Dubai"}'}}]}, finish="tool_calls", usage=usage))
        elif "midstream" in model:
            w.write(self._chunk(model, {"role": "assistant", "content": "Partial "}))
            w.write(b'data: {"error": {"code": 502, "message": "Provider returned error"}}\n\n')
        else:
            if "reason" in model:
                w.write(self._chunk(model, {"role": "assistant", "reasoning": "Thinking about names... "}))
                w.write(self._chunk(model, {"reasoning": "done."}))
            words = text.split(" ")
            for i, wd in enumerate(words):
                piece = wd if i == len(words) - 1 else wd + " "
                w.write(self._chunk(model, {"content": piece}))
                time.sleep(0.005)
            w.write(self._chunk(model, {}, finish="stop", usage=usage))
        w.write(b"data: [DONE]\n\n")
        w.flush()

    def _json(self, status: int, obj: dict):
        data = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def check(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)
    print(f"  ok  {msg}")


def main() -> int:
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{port}/api/v1"
    tmp = tempfile.mkdtemp(prefix="orcmp-")
    try:
        cfg_path = os.path.join(tmp, "req.json")
        with open(cfg_path, "w") as fh:
            json.dump({
                "models": ["mock/alpha", "mock/beta", "mock/gamma", "mock/json-1", "mock/badjson-1", "mock/tool-1",
                           "mock/reason-1", "mock/missing-1", "mock/slow-1", "mock/midstream-1"],
                "messages": [{"role": "system", "content": "Answer briefly."},
                             {"role": "user", "content": "If you built the world's tallest skyscraper, what would you name it?"}],
                "stream": True,
                "tools": [{"type": "function", "function": {"name": "get_weather", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}, "required": ["location"]}}}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "calendar_event", "strict": True, "schema": {
                    "type": "object", "properties": {"name": {"type": "string"}, "date": {"type": "string"}, "participants": {"type": "array", "items": {"type": "string"}}},
                    "required": ["name", "date", "participants"], "additionalProperties": False}}},
            }, fh)

        print("streaming run")
        out = os.path.join(tmp, "run1")
        rc = compare_models.main(["--config", cfg_path, "--out", out, "--base-url", base, "--api-key", "test-key", "--timeout", "1", "--quiet"])
        check(rc == 0, "exit code 0 when at least one model succeeds")
        with open(os.path.join(out, "results.json")) as fh:
            res = json.load(fh)
        by = {r["model_requested"]: r for r in res["results"]}
        check(len(by) == 10, "one record per requested model")
        check(by["mock/alpha"]["ok"] and by["mock/alpha"]["content"] == PROSE["alpha"], "streamed content reassembled verbatim")
        check(by["mock/alpha"]["provider"] == "MockProvider" and by["mock/alpha"]["model_served"] == "mock/alpha-served", "envelope fields captured")
        check(by["mock/alpha"]["usage"]["cost"] == 0.00042, "usage.cost captured")
        check(by["mock/alpha"]["timing"]["ttft_s"] is not None and by["mock/alpha"]["timing"]["ttft_s"] < by["mock/alpha"]["timing"]["latency_s"], "TTFT recorded and below total latency")
        check(by["mock/json-1"]["schema_valid"] is True and by["mock/json-1"]["parsed_json"]["name"] == "Aetherion Spire", "valid structured output parsed and validated")
        check(by["mock/badjson-1"]["schema_valid"] is False and any("missing required" in e for e in by["mock/badjson-1"]["schema_errors"])
              and any("additional property" in e for e in by["mock/badjson-1"]["schema_errors"]), "schema violations reported")
        check(by["mock/alpha"]["schema_valid"] is False, "prose under a json_schema response_format flagged as non-JSON")
        tc = by["mock/tool-1"]
        check(tc["ok"] and tc["tool_calls"][0]["function"]["name"] == "get_weather" and json.loads(tc["tool_calls"][0]["function"]["arguments"]) == {"location": "Dubai"}, "tool-call deltas merged")
        check(by["mock/reason-1"]["reasoning"] == "Thinking about names... done.", "reasoning deltas captured")
        check(not by["mock/missing-1"]["ok"] and by["mock/missing-1"]["http_status"] == 404 and "No endpoints" in by["mock/missing-1"]["error"], "HTTP error surfaced per model")
        check(not by["mock/slow-1"]["ok"] and "timeout" in by["mock/slow-1"]["error"], "timeout surfaced per model")
        check(not by["mock/midstream-1"]["ok"] and "Provider returned error" in by["mock/midstream-1"]["error"], "mid-stream error object surfaced")
        sim = res["metrics"]["similarity"]
        ia, ib, ig = (sim["labels"].index(m) for m in ("mock/alpha", "mock/beta", "mock/gamma"))
        check(sim["matrix"][ia][ib] > sim["matrix"][ia][ig], "alpha closer to beta than to gamma (Jaccard)")
        check(sim["matrix"][ia][sim["labels"].index("mock/missing-1")] is None, "failed models excluded from similarity")
        check(res["metrics"]["rankings"]["fastest_total"] is not None and res["metrics"]["rankings"]["cheapest"]["value"] == 0.00042, "rankings computed")
        check(res["metrics"]["field_agreement"]["name"]["distinct_values"] == 2, "field agreement across structured outputs")
        check(len(res["chart_data"]["latency_s"]["values"]) == 10, "chart series aligned to models")
        for f in ("summary.md", "figures.html"):
            check(os.path.getsize(os.path.join(out, f)) > 1000, f"{f} written")
        check(len(os.listdir(os.path.join(out, "raw"))) == 10, "raw response per model")
        md = open(os.path.join(out, "summary.md")).read()
        check("## Comparison table" in md and "## Failures" in md and "Aetherion Spire" in md, "summary.md has table, failures, outputs")
        fig = open(os.path.join(out, "figures.html")).read()
        check(fig.count("<svg") == 7 and "<table" in fig, "figures.html has six bar charts, heatmap, data table")

        print("non-streaming run with overrides")
        out2 = os.path.join(tmp, "run2")
        rc = compare_models.main(["--model", "mock/alpha", "--model", "mock/gamma", "--prompt", "Name it.", "--system", "Be terse.",
                                  "--out", out2, "--base-url", base, "--api-key", "test-key", "--no-stream", "--quiet"])
        check(rc == 0, "non-stream exit 0")
        with open(os.path.join(out2, "results.json")) as fh:
            res2 = json.load(fh)
        check(res2["run"]["messages"][0] == {"role": "system", "content": "Be terse."}, "--system/--prompt build the messages")
        check(all(r["ok"] for r in res2["results"]) and res2["results"][0]["schema_valid"] is None, "non-stream parse; no schema check without response_format")

        print("all-fail run")
        out3 = os.path.join(tmp, "run3")
        rc = compare_models.main(["--model", "mock/missing-2", "--prompt", "x", "--out", out3, "--base-url", base, "--api-key", "test-key", "--quiet"])
        check(rc == 1, "exit code 1 when every model fails")

        print("unit: --no-response-format / --no-tools strip keys")
        ns = compare_models.parse_args(["--no-tools", "--no-response-format"])
        body = compare_models.build_body({"tools": [1], "response_format": {}, "models": ["a"], "temperature": 0.3}, "m", [], ns)
        check("tools" not in body and "response_format" not in body and "models" not in body and body["temperature"] == 0.3, "keys stripped, others kept")
        print("PASS")
        return 0
    finally:
        server.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
