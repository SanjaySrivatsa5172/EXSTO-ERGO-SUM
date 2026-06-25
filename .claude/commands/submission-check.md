---
description: Pre-submission gate for the manuscript — builds the LaTeX, checks the journal's mechanical requirements, runs consistency, and reports what still blocks submission. Never claims ready until each gate passes.
argument-hint: optional — target journal if not AI and Ethics
---

You are running the pre-submission ritual for this manuscript (target journal:
$ARGUMENTS, default *AI and Ethics*, Springer). This is the analogue of a "clean
PR" — do not declare the manuscript ready until every gate below actually passes.
If a gate fails, stop and report; do not paper over it.

## Gates

1. **Build.** Compile each `.tex` that has a build target (manuscript, condensed,
   charter, online resources, cover letter, title page) with the project's
   LaTeX toolchain (`latexmk -pdf` or `pdflatex`+`bibtex` as the files require).
   Report every error and unresolved `\ref`/`\cite`/`?` warning. A clean PDF is
   not enough — undefined references and missing citations must be zero.
2. **Bibliography.** Every `\cite` resolves to a bib entry; no orphan or
   duplicate entries; DOIs/URLs present where the journal expects them.
3. **Figures & tables.** Every float is referenced in text, has a caption, and
   renders. No "Figure ??".
4. **Front matter.** Title, abstract, keywords, author block, ORCID, and
   affiliation are present and match the README/titlepage/coverletter.
5. **Consistency.** Run the `/consistency` checks (version, counts, terminology,
   cross-references). Surface any mismatch.
6. **Journal mechanics.** Word/page limits, section structure, declarations
   (funding, conflicts, data availability), and the cover letter addresses the
   right editor and journal.

## Output

A checklist with ✅ / ❌ per gate and the exact blocker for each ❌, ordered by
what to fix first. End with one line: **ready to submit** only if every gate is
✅, otherwise **N blockers remain**. Commit nothing and submit nothing — this is
a report. Surfacing problems is the job, not hiding them.
