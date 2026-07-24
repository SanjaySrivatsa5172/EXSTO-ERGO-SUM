---
name: context-engineering
description: >-
  Apply the eight-step context-engineering method (the Karpathy–Cherny
  approach): a curated CLAUDE.md context layer, task specs instead of prompts,
  subagent fan-out, deterministic verification hooks, a compounding
  learnings.md, /goal + /loop heartbeats, scheduled Routines, and orchestrated
  multi-agent workflows. Use this whenever the user mentions context
  engineering or "the playbook"; asks to create, audit, or slim down a
  CLAUDE.md; wants a task turned into a proper spec; asks for hooks that
  auto-format code or block finishing until tests pass; wants Claude to
  remember lessons across sessions; asks about /loop, /goal, scheduled
  routines, or wide multi-agent sweeps; or says anything like "set up my
  repo/project so Claude works better", even if they never say the words
  "context engineering". Also consult it before starting substantial
  multi-step work in a repository that has no CLAUDE.md yet.
---

# Context Engineering

Turn "write a good prompt" into "design everything the model sees." The method
has eight layers; each one is an artifact you can create, audit, or improve.

| # | Layer | Artifact | Why it exists |
|---|-------|----------|---------------|
| 1 | Context layer | `CLAUDE.md` + `.claude/rules/` | conventions survive across sessions |
| 2 | Spec | goal / scope / deliverables / stop condition | decisions stay with the user |
| 3 | Subagents | fan-out with clean windows | the plan doesn't drown in diffs |
| 4 | Hooks | formatter + Stop-gate verifier | non-negotiables get enforced, not suggested |
| 5 | Learnings | `learnings.md`, promoted to rules | context compounds run over run |
| 6 | Heartbeat | `/goal` + `/loop` | work continues until a checkable state |
| 7 | Routines | cloud schedules (cron / webhook / GitHub event) | work continues after the session ends |
| 8 | Fleets | workflow scripts with verification | coordination lives in code, not context |

The full method — reasoning, worked examples, cadence table — is in
`references/playbook.md`. Read it when the user wants explanation or when a
play below needs more detail than this file carries.

## First move: diagnose

Before changing anything, check which layers already exist in the working
repository and report a short gap table:

- `CLAUDE.md` — present? line count? (over ~200 lines means it needs cutting,
  not adding)
- `.claude/rules/` — any scoped rules?
- Hook configuration in `.claude/settings.json` — formatter on `Write|Edit`?
  a `Stop` verifier wired to the real test command?
- `learnings.md` (or equivalent) — present and imported from `CLAUDE.md`?
- Any Routines / scheduled automation for this project?

Then recommend the one or two layers with the highest payoff for this project.
Do not scaffold all eight at once — an empty ritual file teaches the user to
ignore the system.

## Plays

Match the user's ask to a play. Each play states the intent, the action, and
where to look for detail.

**Set up or slim the context layer.** Scaffold `CLAUDE.md` from the real
project (stack, test/lint/type commands, hard rules). Every line must be
earned; move path-specific rules to `.claude/rules/*.md`. When trimming an
existing file, propose deletions with reasons rather than deleting silently.

**Turn a request into a spec.** Copy `assets/spec-template.md` and fill it
from the user's words, asking only for what cannot be inferred. The stop
condition must be objectively checkable (tests green, grep returns nothing,
build passes) — if the user gives a vague goal, negotiate it into a checkable
one before starting work.

**Split work across subagents.** When a task spans many files or the context
is filling with diffs and logs, fan out one subagent per unit (file, module,
route). Instruct each to do the work, verify it locally, and report back only:
what changed, and anything failing. Exceptions, not transcripts.

**Install the verifier gate.** Adapt `assets/hooks.example.json` to the
project's real formatter and test commands, then merge it into
`.claude/settings.json` — show the user the exact JSON before writing it,
since hooks execute automatically from then on. The `Stop` hook is the piece
that converts "I'm done" into "it's verified."

**Start the learnings loop.** Create `learnings.md`, import it from
`CLAUDE.md` (`@learnings.md`), and at the end of each task append 1–3 dated,
action-first one-liners. When a failure repeats an entry already in the file,
promote it into `CLAUDE.md` as a hard rule. Keep entries to one line — short
entries get used, paragraphs get skipped.

**Give active work a heartbeat.** Define the finish line with `/goal`
(checkable state), the cadence with `/loop` (interval + what to check + what
to fix). Always include what to do when the goal is met: say so once, stop.

**Promote recurring checks to Routines.** Any check the user repeats weekly by
hand becomes a scheduled Routine (claude.ai/code/routines or `/schedule`).
Write the routine prompt as a complete standalone instruction — a fresh
session runs it with no memory of this conversation.

**Scale to a fleet.** For work wider than one context window (audits,
migrations, sweeps), write the coordination as a workflow script: fan out
parallel subagents, cross-check findings adversarially, merge one verified
report. Only reach for this when the user has opted into multi-agent scale.

## Guardrails

- More context is not better context; curation is the job. Never respond to a
  failure by dumping more text into `CLAUDE.md`.
- Hooks and settings changes run code automatically — always show the user
  what will be written and where before writing it.
- The verifier gate is not optional decoration: a playbook setup without a
  real test command wired into it is theater. If the project has no tests,
  say so and gate on the best available check (build, lint, typecheck).
