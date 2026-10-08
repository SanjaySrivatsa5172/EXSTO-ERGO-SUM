# Cardiovascular Research Vault — CLAUDE.md

## Purpose
A knowledge graph for cardiovascular research. Each note is a finding, concept,
trial, or hypothesis; each link is a relationship between them. The goal is not to
file papers. The goal is to turn scattered findings into understanding — patterns,
contradictions, and testable hypotheses you would not see one trial at a time.

## Core principle
A finding stored in isolation is just a fact. A finding connected to others becomes
evidence — it supports, contradicts, or refines a claim. Every note should connect
to at least one other note.

## Claude's role
When asked, do these and nothing else unless told:
1. **Connect** — non-obvious links between a note and existing notes
   (supports / contradicts / mechanism-for / confounds / refines).
2. **Contradict** — actively surface where trials/findings disagree (e.g. anatomy
   vs. physiology, revascularization vs. medical therapy). Contradiction marks the
   open question.
3. **Question** — application questions: trial design, mechanism, endpoint choice,
   what would change the conclusion. Never "define X."
4. **Hypothesize** — when asked, propose testable hypotheses the graph implies.
5. **Schedule** — update each note's `review` date using the interval ladder.
6. **Synthesize** — integrate a topic into one written mini-review on request.

## What Claude never does
Never restate an abstract as a "summary." Never present a contested clinical claim
as settled when the notes disagree — surface the disagreement and what trial would
resolve it. Flag anything needing source/citation verification rather than smoothing
it over.

## The note format
Notes live in `findings/`. Frontmatter is six fields:

```
---
topic: <area, e.g. coronary physiology>
type: concept | trial | dataset | hypothesis
source: <citation, trial name, dataset, or "own data">
created: YYYY-MM-DD
review: YYYY-MM-DD
mastery: 0        # 0–5, confidence you understand it well enough to use it
---
```

Body sections (your own words):
- **In my words** — the finding/concept as you'd explain it. The gap where you
  can't is the thing to chase.
- **Why it matters** — what it changes: a decision, a mechanism, a prediction.
- **Strength & caveats** — evidence level, population, confounders, what would
  overturn it.
- **Connections** — `[[links]]` (Claude adds these).
- **Questions** — application / hypothesis questions (Claude adds these).

## Review interval ladder
1 → 3 → 7 → 14 → 30 → 60 days. Solid recall moves up a rung; a miss drops one.

## The two prompts
See `README.md`: a **daily** prompt (connect + contradict + question + schedule)
and a **synthesis** prompt (run per topic to integrate and generate hypotheses).
