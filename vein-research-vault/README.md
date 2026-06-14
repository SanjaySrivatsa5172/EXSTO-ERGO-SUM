# Vein Research Vault

A research-oriented twin of the `learning-vault/` method — same simplified
machinery (2 folders, lean frontmatter, 2 prompts), tuned for **building
understanding across venous research data** instead of studying a fixed subject.

The difference from the learning vault: it doesn't just help you *retain* a
subject, it helps you *interrogate* a body of findings — surfacing contradictions
between studies and generating testable hypotheses.

- **2 folders** — `findings/` (one note per finding/concept/study/hypothesis) and
  `synthesis/` (mini-reviews)
- **6-field frontmatter** — `topic`, `type`, `source`, `created`, `review`, `mastery`
- **2 prompts** — daily and synthesis (below)

> Setup (iCloud-only vs. Obsidian-on-top): see `SETUP.md`.

## How to use it

1. **Capture a finding.** Copy `_finding-template.md` into `findings/`, rename it,
   and write *In my words* + *Strength & caveats* yourself. For your own data, put
   `source: own data` and record n / design / what's still unverified.
2. **Run the daily prompt** so Claude links it, flags contradictions, questions
   you, and dates the review.
3. **Answer the questions cold**, then check.
4. **Per topic, run the synthesis prompt** to integrate and generate hypotheses.

## Seed notes are stubs, not gospel
The starter notes in `findings/` are scaffolding written quickly to give the graph
something to connect on day one. **You are the domain expert — rewrite each one in
your own words and verify every clinical claim and citation.** That rewrite *is*
the learning step; the stub just removes the blank page.

---

## Prompt 1 — Daily (connect + contradict + question + schedule)

> I've added or updated notes in `findings/` today. For each new or changed note:
> 1. **Connect** — find 1–3 *non-obvious* links to other notes in `findings/`.
>    Label each as supports / contradicts / mechanism-for / confounds / refines,
>    one sentence on the specific relationship. Add under **Connections** as `[[links]]`.
> 2. **Contradict** — explicitly flag any note whose findings disagree with this
>    one, and say what would resolve the disagreement.
> 3. **Question** — under **Questions**, write 2–3 *application* questions (study
>    design, mechanism, or "what result would change the conclusion"). Never "define X."
> 4. **Schedule** — set `review` using the ladder (1→3→7→14→30→60 days, by `mastery`).
>
> Then list notes with `review` due today or earlier, lowest `mastery` first, and
> flag anything where I should verify the source.

## Prompt 2 — Synthesis (per topic — integrate + hypothesize)

> I've been building notes on **[topic]**. They cover **[list main areas]**.
> Run a synthesis session:
> 1. **Patterns** — what recurs across these findings that no single note states?
> 2. **Contradictions** — where do the findings genuinely disagree, and what study
>    would resolve each?
> 3. **Mechanism** — the single relationship that, if I understood it fully, would
>    tie the most findings together.
> 4. **Hypotheses** — generate 3 *testable* hypotheses the graph implies. For each:
>    the prediction, the minimal study/dataset to test it, and what would falsify it.
> 5. **Gaps** — given what I have, what evidence would most increase understanding next?
> 6. Write a 400–600 word **mini-review** integrating the strongest findings, with
>    caveats stated, and save it to `synthesis/[topic]-synthesis.md`.

---

## Notes on `type` and `mastery`
- `type: study` for a single paper/trial; `dataset` for your own data; `concept`
  for a mechanism or definition; `hypothesis` for something you're proposing.
- `mastery` = your confidence you understand it well enough to *use* it in an
  argument or design — not whether you've memorized it.
