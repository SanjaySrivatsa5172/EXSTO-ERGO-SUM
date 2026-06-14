# Learning Vault (simplified)

A stripped-down version of the Obsidian + Claude "learning vault" method. The
original used 7 folders, a 6-field frontmatter, and 5 prompts. This keeps the
parts that actually drive learning and drops the ceremony:

- **2 folders** — `concepts/` (one note per idea) and `synthesis/` (integration docs)
- **4-field frontmatter** — `subject`, `created`, `review`, `mastery`
- **2 prompts** — one daily, one biweekly

## How to use it (≈30 min/study session)

1. **Write a concept note.** Copy `_concept-template.md` into `concepts/`,
   rename it for the idea, and write the *In my words* section yourself. Where
   you can't write it cleanly is exactly the thing you don't understand yet.
2. **Run the daily prompt** (below) so Claude links it, questions you, and dates
   the review.
3. **Answer the recall questions cold** — write your answer before re-reading the
   note. Then check.
4. **Every ~2 weeks per subject, run the synthesis prompt** to integrate.

That's the whole system. Three actions per concept; the compression in learning
time comes from never re-reading material you've already retained.

---

## Prompt 1 — Daily (connect + question + schedule)

> I've added or updated concept notes in `concepts/` today. For each new or
> changed note:
> 1. **Connect** — find 1–3 *non-obvious* links to other notes in `concepts/`.
>    Non-obvious = not stated in either note, not surface "related to." Add them
>    under **Connections** as `[[links]]`, each with one sentence naming the
>    specific relationship.
> 2. **Question** — under **Recall**, write 2–3 *application* questions. Never
>    "define X." A good question requires using the concept in a new situation
>    and can't be answered by someone who only memorized the definition.
> 3. **Schedule** — set `review` using the ladder (1→3→7→14→30→60 days from
>    today, by current `mastery`).
>
> Also tell me which notes are `review` due today or earlier, hardest first.

## Prompt 2 — Synthesis (every ~2 weeks, per subject)

> I've been studying **[subject]**. My concept notes cover **[list main areas]**.
> Run a synthesis session:
> 1. **Patterns** — what recurs across these notes that no single note states?
> 2. **Deepest connection** — the one relationship that ties the most concepts
>    together; what would I miss if I never understood it?
> 3. **Predictions** — from what I've learned, generate 3 novel scenarios and ask
>    *me* to predict the outcome before you evaluate.
> 4. **Gaps** — what, given what I know, would most increase my understanding next?
> 5. Write a 400–600 word **synthesis document** integrating the most important
>    concepts into one coherent account, and save it to
>    `synthesis/[subject]-synthesis.md`.

---

## Mastery / review rules
- `mastery` 0–5. Correct cold recall: +1 and move `review` up one rung. Miss: −1
  and drop one rung.
- A concept missed repeatedly goes into the next synthesis session, not just more
  repetition.

## Why these two methods
Active recall (retrieval, not re-reading) and spaced repetition (reviewing at the
edge of forgetting) are the two best-evidenced study techniques. Everything here
is just plumbing to make you do both consistently.
