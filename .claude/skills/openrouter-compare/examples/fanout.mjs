#!/usr/bin/env node
// Minimal Node equivalent of the fan-out. Reads an OpenRouter chat/completions
// body (with a `models` array) and sends it once per model, concurrently.
// The full comparison, Markdown, and chart export live in
// ../scripts/compare_models.py; this file shows the request pattern only.
//
//   OPENROUTER_API_KEY=... node examples/fanout.mjs examples/skyscraper.json > out.json

import { readFileSync } from "node:fs";

const url = (process.env.OPENROUTER_BASE_URL ?? "https://openrouter.ai/api/v1") + "/chat/completions";
const cfgPath = process.argv[2];
if (!cfgPath) {
  console.error("usage: node fanout.mjs <request.json>");
  process.exit(2);
}
if (!process.env.OPENROUTER_API_KEY) {
  console.error("error: set OPENROUTER_API_KEY");
  process.exit(2);
}

const cfg = JSON.parse(readFileSync(cfgPath, "utf8"));
const { models, model, route, ...template } = cfg;
const ids = models ?? (model ? [model] : []);
if (ids.length === 0) {
  console.error("error: config needs a `models` array or a `model`");
  process.exit(2);
}

// Non-streaming keeps this example short; the Python tool streams to measure TTFT.
const body = { ...template, stream: false, usage: { include: true, ...(template.usage ?? {}) } };

async function callOne(id) {
  const t0 = performance.now();
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ...body, model: id }),
    });
    const data = await res.json();
    const latency_s = (performance.now() - t0) / 1000;
    if (!res.ok || data.error) {
      return { model: id, ok: false, http_status: res.status, error: data.error?.message ?? res.statusText, latency_s };
    }
    const choice = data.choices?.[0] ?? {};
    return {
      model: id,
      ok: true,
      model_served: data.model,
      provider: data.provider,
      content: choice.message?.content ?? "",
      tool_calls: choice.message?.tool_calls ?? [],
      finish_reason: choice.finish_reason,
      usage: data.usage,
      latency_s,
    };
  } catch (err) {
    return { model: id, ok: false, error: String(err), latency_s: (performance.now() - t0) / 1000 };
  }
}

const results = await Promise.all(ids.map(callOne));
for (const r of results) {
  const tag = r.ok ? "ok  " : "FAIL";
  const tail = r.ok ? `${r.usage?.completion_tokens ?? "?"} tok, $${r.usage?.cost ?? "?"}` : r.error;
  console.error(`${tag} ${r.model.padEnd(45)} ${r.latency_s.toFixed(2)} s  ${tail}`);
}
console.log(JSON.stringify({ endpoint: url, request_template: body, results }, null, 2));
