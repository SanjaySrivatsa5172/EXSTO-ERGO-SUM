# The Context Engineering Playbook

**The Karpathy–Cherny method, rebuilt as a working manual.**

*Concept lineage: Andrej Karpathy's "context engineering" reframing of prompt-writing, and Boris Cherny's Claude Code working practices (persistent context files, deterministic verification). Structure inspired by [this X deep-dive](https://x.com/vartekxx/status/2074864291568664646); the text and every example below are written from scratch.*

---

## The operating idea

Prompting optimizes one sentence. Context engineering designs **everything the model sees** — the standing rules, the task spec, the tools, the feedback, the memory. The aphorism (Karpathy's): *the context window is your program.* You are still the programmer.

The eight steps below turn that idea into a daily workflow. Steps 1–4 build the machine, steps 5–8 make it run by itself.

---

## Step 1 — Lay down the context layer (`CLAUDE.md`)

`CLAUDE.md` loads at the start of every session. Without it, each session rediscovers your conventions from zero — and rediscovers them differently each time.

Scaffold it, then curate hard:

```bash
claude /init
```

```markdown
# Project: billing-service
# Stack: Python 3.12, FastAPI, PostgreSQL, SQLAlchemy

Test:  pytest -q
Lint:  ruff check .
Types: mypy --strict src/

## Rules
- Repository pattern only — handlers never touch the ORM session directly
- Every public endpoint gets a rate-limit decorator
- Money is Decimal, never float
- A new env var lands in config.py AND .env.example in the same commit
- Run the test suite before every commit
```

Curation rules:

- **Every line must be earned.** A lean file the model actually follows beats a 2,000-line dump it skims. Stay under ~200 lines.
- Rules that only apply to one path or file type go in `.claude/rules/*.md`, not the main file.
- Prune monthly. A stale rule teaches the model to ignore the file.

---

## Step 2 — Write specs, not wishes

A one-line prompt silently delegates every decision you care about. A spec keeps them. The anatomy: **goal, scope in, scope out, deliverables, conflict policy, stop condition.**

```text
# Task: Move service config from YAML files to environment variables

GOAL: All runtime config read from env vars via config.py;
      the YAML loaders are deleted.

SCOPE
- IN:  src/config/, src/services/, tests/
- OUT: infra/helm/ (values files stay), docs/

DELIVERABLES
- config.py with typed accessors and defaults
- .env.example updated to match
- Tests updated; no test reads a YAML fixture

ON CONFLICT: stop and name the file — do not resolve silently
STOP WHEN: pytest green, mypy clean, grep finds no yaml.load
```

The stop condition is the most important line: it converts "make it better" into a checkable state.

---

## Step 3 — Firewall context with subagents

A long task in a single window fills that window with diffs, logs, and dead ends until the plan drowns. Subagents give each subtask a fresh context; the main thread keeps only the plan and the outcomes.

```text
Split the endpoint audit by router file.
For each file, spawn a subagent that:
  - checks every handler for auth and rate limiting,
  - fixes the gaps,
  - runs that file's tests.
Report back only: file, what changed, anything still failing.
```

The pattern to remember: **report exceptions, not transcripts.**

---

## Step 4 — Gate with hooks (the verifier)

Everything in `CLAUDE.md` is advisory — followed most of the time, not all of it. Hooks are enforced by the harness on every matching event, every time. Anything non-negotiable belongs in a hook.

Two workhorses — format on every write, and refuse to finish until the suite is green:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs -r ruff format"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Run pytest -q. Fix and re-run until green, then allow the stop."
          }
        ]
      }
    ]
  }
}
```

Notes: command hooks receive a JSON payload on stdin (hence `jq`). The `Stop` hook is the piece that turns "I'm done" into "it's verified" — no human in the loop.

---

## Step 5 — Compound with a learnings file

The context should get better every run, not reset to zero. End every task with a short ritual:

```text
When the task completes:
1. Check the result against the spec's STOP WHEN line.
2. Note what worked and what needed a retry.
3. Append 1–3 dated one-liners to learnings.md.
4. If a failure repeats something already logged there,
   promote it into CLAUDE.md as a hard rule.
```

```markdown
# learnings.md — imported by CLAUDE.md via @learnings.md
2026-07-18: Stripe test clocks drift — freeze time in payment tests.
2026-07-21: Alembic autogenerate misses enum changes; write those by hand.
2026-07-23: /reports endpoints are unauthenticated BY DESIGN — do not "fix".
```

Keep entries dated, action-first, one line each. Short entries get used; paragraphs get skipped. This is the compounding loop: each run writes what the next run reads.

---

## Step 6 — Give the loop a heartbeat (`/goal` + `/loop`)

`/goal` defines when the work is finished. `/loop` defines how often to push toward it. Together they make an agent that keeps working until the state is reached.

```text
/goal every public endpoint rate-limited and the test suite green

/loop every 10m: run pytest. Fix any failure you find,
then re-check the goal. If the goal is met, say so once and stop.
```

The same shape babysits a pull request:

```text
/loop every 5m: check PR #142.
CI red   → read the failing job log, fix, push.
New review comment → address it and resolve the thread.
All green, no comments → reply with a one-line status.
```

---

## Step 7 — Outlive the terminal (Routines)

A `/loop` ends when the session does. Routines run on Anthropic's infrastructure on a schedule — laptop closed, terminal gone. Three trigger types: **schedule (cron), API call (webhook), GitHub event.** Set up at `claude.ai/code/routines` or with `/schedule`.

```text
Mondays 08:00 UTC:
Diff the dependency lockfile against last week's.
For each bump, scan the release notes for breaking changes and CVEs.
Open one PR with the safe upgrades.
File an issue listing anything risky.
Nothing to change → report "clean".
```

Rule of thumb: any check you'd repeat weekly by hand is a routine you haven't written yet.

---

## Step 8 — Scale with orchestrated fleets

When the work is wider than one context window can hold, put the coordination in **code**, not in the conversation: a workflow script fans out parallel subagents, cross-checks their findings, and merges one verified result. Tokens go to work, not to coordination overhead.

```text
Audit every handler in src/api/ for missing input validation.
Wave 1: one agent per file — report each gap with a line number.
Wave 2: adversarial reviewers re-check every finding and drop
        anything that does not reproduce.
Merge into a single report: file · line · severity.
```

---

## What this does not fix

- **Bloated context is its own failure mode.** Past a point, more context buries the signal. Curation is the job.
- **Perfect context still hallucinates.** Less often — not never. The verifier gate (Step 4) is not optional.
- **It is a skill, and it is practiced.** The question is never "what do I want to say" but "what does the model need to see."

---

## The cadence at a glance

| When | Do | Mechanism |
|---|---|---|
| Session start | standing context loads | `CLAUDE.md` + `.claude/rules/` |
| Every task | write the spec first | goal / scope / stop condition |
| Big tasks | split into clean windows | subagents |
| Always | enforce, don't remind | hooks |
| Task end | log 1–3 learnings, promote repeats | `learnings.md` |
| Active work | heartbeat until done | `/goal` + `/loop` |
| Off-hours | scheduled runs in the cloud | Routines |
| Wide sweeps | coordination as code | workflow scripts |

## Setup checklist

- [ ] `claude /init`, then cut `CLAUDE.md` to fewer than 200 earned lines
- [ ] `.claude/rules/` holds the path-scoped rules
- [ ] Formatter hook on `Write|Edit`
- [ ] `Stop`-hook verifier wired to the real test command
- [ ] `learnings.md` created and imported from `CLAUDE.md`
- [ ] One weekly hand-done check promoted to a Routine

---

*A prompt is what you say. Context is what the model knows. Engineer the second, and the first gets very short.*
