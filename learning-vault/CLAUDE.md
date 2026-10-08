# Learning Vault — CLAUDE.md

## Purpose
This vault is a knowledge graph for active learning. Every idea is a note; every
relationship between ideas is a link. The goal is not to store information. The
goal is to build understanding through connection.

## Core principle
A fact stored in isolation is forgotten. A fact connected to several others is
retained. Every concept added should connect to at least one existing concept.

## Claude's role
When asked, do these four things and nothing else unless told:
1. **Connect** — find non-obvious links between a new note and existing notes.
2. **Question** — generate *application* recall questions (never "define X").
3. **Schedule** — update each note's `review` date using the interval ladder.
4. **Synthesize** — on request, integrate a subject into one written document.

## What Claude never does
Never write a summary that just restates the source — summaries don't produce
learning, connections do. If a concept note links to nothing, it is incomplete.

## The note format
Notes live in `concepts/`. Frontmatter is exactly four fields:

```
---
subject: <area>
created: YYYY-MM-DD
review: YYYY-MM-DD
mastery: 0        # 0–5, raised on correct recall, lowered on miss
---
```

Body sections (keep short, your own words):
- **In my words** — explain it as if teaching someone. If you can't, that's the gap.
- **Why it matters** — the problem it solves / prediction it enables.
- **Connections** — `[[links]]` to other notes (Claude adds these).
- **Recall** — application questions (Claude adds these); answers hidden below `---`.

## Review interval ladder
1 → 3 → 7 → 14 → 30 → 60 days. Correct recall moves up one rung; a miss drops
one rung. A concept missed repeatedly is flagged for the next synthesis session.

## The two prompts
Everything runs on just two prompts — see `README.md`:
- **Daily prompt** — does connect + question + schedule in one pass.
- **Synthesis prompt** — run every ~2 weeks per subject.
