# Cardiovascular Research Vault

A research-oriented vault — same simplified machinery as `learning-vault/` and a
twin of `vein-research-vault/`, tuned for **building understanding across
cardiovascular research data**: surfacing contradictions between trials and
generating testable hypotheses.

- **2 folders** — `findings/` (one note per finding/concept/trial/hypothesis) and
  `synthesis/` (mini-reviews)
- **6-field frontmatter** — `topic`, `type`, `source`, `created`, `review`, `mastery`
- **2 prompts** — daily and synthesis (below)

> Setup (iCloud-only vs. Obsidian-on-top): see `SETUP.md`.

## How to use it

1. **Capture a finding.** Copy `_finding-template.md` into `findings/`, rename it,
   and write *In my words* + *Strength & caveats* yourself. For your own data, set
   `source: own data` and record n / design / what's still unverified.
2. **Run the daily prompt** so Claude links it, flags contradictions, questions you,
   and dates the review.
3. **Answer the questions cold**, then check.
4. **Per topic, run the synthesis prompt** to integrate and generate hypotheses.

## Seed notes are stubs, not gospel
The starter notes in `findings/` are scaffolding to give the graph something to
connect on day one. **You are the domain expert — rewrite each one in your own
words and verify every clinical claim and citation.** That rewrite *is* the
learning step; the stub just removes the blank page.

---

## Prompt 1 — Daily (connect + contradict + question + schedule)

> I've added or updated notes in `findings/` today. For each new or changed note:
> 1. **Connect** — 1–3 *non-obvious* links to other notes in `findings/`, each
>    labelled supports / contradicts / mechanism-for / confounds / refines with one
>    sentence on the specific relationship. Add under **Connections** as `[[links]]`.
> 2. **Contradict** — flag any note whose findings disagree with this one, and say
>    what trial or analysis would resolve the disagreement.
> 3. **Question** — under **Questions**, write 2–3 *application* questions (trial
>    design, mechanism, endpoint choice, or "what result would change the conclusion").
>    Never "define X."
> 4. **Schedule** — set `review` using the ladder (1→3→7→14→30→60 days, by `mastery`).
>
> Then list notes with `review` due today or earlier, lowest `mastery` first, and
> flag anything where I should verify the source.

## Prompt 2 — Synthesis (per topic — integrate + hypothesize)

> I've been building notes on **[topic]**. They cover **[list main areas]**.
> Run a synthesis session:
> 1. **Patterns** — what recurs across these findings that no single note states?
> 2. **Contradictions** — where do trials genuinely disagree, and what study resolves each?
> 3. **Mechanism** — the single relationship that, fully understood, ties the most
>    findings together.
> 4. **Hypotheses** — 3 *testable* hypotheses the graph implies. For each: the
>    prediction, the minimal trial/dataset to test it, and what would falsify it.
> 5. **Gaps** — what evidence would most increase understanding next?
> 6. Write a 400–600 word **mini-review** integrating the strongest findings, caveats
>    stated, saved to `synthesis/[topic]-synthesis.md`.

---

## Notes on `type` and `mastery`
- `type: trial` for a single study; `dataset` for your own data; `concept` for a
  mechanism/definition; `hypothesis` for something you're proposing.
- `mastery` = confidence you understand it well enough to *use* it in an argument or
  trial design — not whether you've memorized it.
