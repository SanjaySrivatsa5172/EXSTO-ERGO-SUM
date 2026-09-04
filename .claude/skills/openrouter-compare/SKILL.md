---
name: openrouter-compare
description: Send one prompt to several OpenRouter models, compare their outputs, and export a Markdown summary, a structured results.json (per-model records, metrics, similarity matrix, chart-ready series), and a self-contained figures.html with SVG charts. Use when the user wants to compare, benchmark, or A/B LLMs through OpenRouter (latency, time to first token, tokens, cost, output length, agreement, structured-output compliance, tool-call behaviour), or pastes an OpenRouter chat/completions curl with a `models` array and asks to compare the models' answers. Standard library Python; needs OPENROUTER_API_KEY.
---

# OpenRouter multi-model compare

Fan one chat request out to N models on OpenRouter, one request per model in
parallel, then compare and export.

Why a separate request per model: OpenRouter's `models` array is a **fallback
chain**, not a fan-out. A single request with nine models is answered by the first
model that accepts it; you get one answer, not nine. The script takes the same
request body, strips `models`, and sends it once per model with `model` set.

## Prerequisites

- Python 3.9+ (standard library only, no pip installs).
- `OPENROUTER_API_KEY` in the environment (or `--api-key`).
- Optional attribution headers: `OPENROUTER_REFERER`, `OPENROUTER_TITLE`.

## Usage

```bash
# From an OpenRouter request body (the JSON you would pass to curl -d)
python3 scripts/compare_models.py --config examples/skyscraper.json --out runs/skyscraper

# Ad hoc, no config file
python3 scripts/compare_models.py \
  --model anthropic/claude-fable-5.1 --model x-ai/grok-4.6 --model google/gemini-3.8-flash \
  --system "Answer concisely." \
  --prompt "If you built the world's tallest skyscraper, what would you name it?" \
  --out runs/skyscraper-quick

# Reuse a config but drop the parts that make the comparison unfair
python3 scripts/compare_models.py --config request.json --no-response-format --no-tools
```

Paths are relative to this skill's directory.

| Flag | Default | Meaning |
|---|---|---|
| `--config FILE` | none | An OpenRouter `chat/completions` body: `models`/`model`, `messages`, `tools`, `response_format`, `temperature`, `reasoning`, ... All keys except `models`, `model`, `route` are forwarded unchanged. |
| `--model ID` | from config | Repeatable. Overrides the config's model list. IDs are passed verbatim. |
| `--prompt TEXT` | from config | Replaces `messages` with a single user turn (plus `--system`). |
| `--system TEXT` | from config | Replaces any system message. |
| `--out DIR` | `runs/<UTC timestamp>` | Output directory. |
| `--title TEXT` | first 60 chars of the prompt | Title for the summary and figures. |
| `--timeout S` | `180` | Per-request timeout. A slow model fails alone; the run continues. |
| `--concurrency N` | `8` | Simultaneous requests. |
| `--no-stream` | off | Disable SSE streaming. Time to first token is then unavailable. |
| `--no-tools` | off | Drop `tools` and `tool_choice`. |
| `--no-response-format` | off | Drop `response_format`. |
| `--base-url URL` | `https://openrouter.ai/api/v1` | Any OpenAI-compatible endpoint (also `OPENROUTER_BASE_URL`). |

Exit codes: `0` at least one model succeeded, `1` every model failed, `2` bad
arguments or missing key.

## Outputs

```
<out>/
  summary.md      run metadata, prompt, comparison table, rankings, pairwise
                  similarity, field agreement (structured output), every
                  model's full output, reasoning, tool calls, schema
                  violations, failures
  results.json    schema_version, run (messages, request template, options),
                  results[] (one record per model: content, reasoning,
                  tool_calls, usage, finish_reason, parsed_json,
                  schema_valid, timing, error), metrics (per_model, rankings,
                  similarity matrix, field_agreement), chart_data (labels +
                  values per measure, ready for any plotting library)
  figures.html    self-contained page: horizontal bar charts for latency, time
                  to first token, completion tokens, decode throughput, cost,
                  output length; Jaccard similarity heatmap; data table.
                  Light and dark themes. No external assets.
  raw/<model>.json  verbatim response, or the list of SSE chunks when streaming
```

### What is measured

- **Latency** wall-clock from request to last byte. **TTFT** time to the first
  content, reasoning, or tool-call delta (streaming only).
- **Tokens and cost** from OpenRouter's `usage` block. The script sets
  `usage.include = true` so `usage.cost` (USD) is returned. Reasoning tokens are
  recorded when the provider reports them.
- **Decode throughput** completion tokens divided by (latency minus TTFT). Not
  computed when that interval is under 50 ms.
- **Similarity** Jaccard index over lower-cased word sets (words longer than two
  characters). Lexical only; two paraphrases with different vocabulary score low.
  "Most consensual" is the model with the highest mean similarity to the others.
- **Structured output** when `response_format` is `json_schema` or `json_object`,
  each output is parsed (tolerating a ```json fence) and checked against a
  subset of JSON Schema: `type`, `properties`, `required`,
  `additionalProperties: false`, `items`, `enum`. **Field agreement** groups
  the values each model produced for each top-level field.
- **Tool calls** are captured with merged streaming deltas. A model that only
  calls a tool counts as a success with zero words of content.

### Failure handling

Each model fails independently: HTTP errors (unknown model ID, no endpoint,
rate limit), timeouts, and OpenRouter's mid-stream `{"error": ...}` objects are
recorded in the model's record and listed under **Failures**. Failed models
appear in every table with `n/a` and are excluded from the similarity matrix,
rankings, and charts.

## Interpreting the example

`examples/skyscraper.json` reproduces a request pasted from the OpenRouter
playground: nine models, a `get_weather` tool the prompt never needs, and a strict
`calendar_event` JSON schema that has nothing to do with the question. Run as-is
it measures how each model reconciles an unrelated strict schema with a free-text
question (most will force the answer into `name` and invent `date` and
`participants`). Run with `--no-response-format --no-tools` for a plain answer
comparison. Model IDs in that file are passed through verbatim; an ID OpenRouter
does not recognise fails with HTTP 400 or 404 for that model only.

## Self-test

No key required. Spins up a mock OpenRouter on localhost and exercises
streaming, non-streaming, tool calls, reasoning deltas, schema validation, HTTP
errors, timeouts, and mid-stream errors:

```bash
python3 scripts/selftest.py
```

## Notes

- The Markdown summary uses tables because it is meant to be read on GitHub;
  `figures.html` and `results.json` are the sources for figures and further
  analysis.
- Costs are OpenRouter's accounting for the run; they exclude cached-prompt
  discounts unless the provider reports them in `usage`.
- Keep `runs/` out of version control (already in this skill's `.gitignore`)
  unless a specific run is meant to be a durable record; then commit its
  `summary.md` and `results.json` deliberately.
