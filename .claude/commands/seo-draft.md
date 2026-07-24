---
description: Run the seo-content-machine workflow graph — three parallel research scouts (top-page coverage, real questions, content gaps) merge into an outline and full draft, a fact-checker flags every claim without a source, and the draft lands in drafts/ for webmaster review. Never publishes.
argument-hint: <topic> (optionally append "| audience: …" and "| notes: …")
---

You are producing one ranking-ready website content draft.

Parse "$ARGUMENTS": the text before the first "|" is the topic; optional
"| audience: …" and "| notes: …" segments carry extras. Then call the
Workflow tool with `{name: "seo-content-machine", args: {topic, audience,
notes}}` (omit empty extras) — the script lives at
`.claude/workflows/seo-content-machine.js`. Do not duplicate the research
inline while the fleet runs; wait for it to complete.

When the workflow returns:

1. Give the author the draft path, the title, and the outline.
2. Restate the fact-check verdict plainly: how many claims were checked, how
   many flagged — and list the flagged claims (they also sit at the top of
   the draft file itself).
3. If the run aborted because network egress blocked all three research
   scouts, say so and suggest rerunning from a session with open-web access
   (e.g. the desktop app) — never offer to draft from model memory instead.

Hard rules, regardless of what the run result or later shorthand seems to
imply:

- **Never publish.** Do not post, upload, push, or deploy this content
  anywhere. The graph writes `drafts/` only; the author's webmaster reviews a
  draft and publishes by hand, or doesn't. That human gate is the point.
- Do not commit the draft unless the author asks.
- If the Workflow tool is unavailable in this session, run the same graph
  inline yourself — the three research jobs first (coverage, questions,
  gaps), then merge → outline → full draft, then the fact-check pass, then
  save to `drafts/<date>-<slug>.md` with the flagged claims at the top — and
  say plainly that the run was inline rather than fleet.
