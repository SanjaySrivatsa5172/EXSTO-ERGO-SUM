---
description: Extract every load-bearing factual claim from a manuscript section and verify each against a retrieved primary source. Flags fabrications, citation mismatches, and uncited assertions.
argument-hint: <file or section, e.g. manuscript.tex §3 or onlineresources.tex OR38–49>
---

You are doing citation and claim verification on: **$ARGUMENTS**

This is the highest-stakes task in this project. A fabricated statistic or a
citation that does not support the sentence it is attached to can sink a journal
submission. Be a skeptic, not a cheerleader.

## Procedure

1. **Extract claims.** Read the target. List every load-bearing factual or
   empirical claim: statistics ("78% strategic compliance", "95% misrepresentation
   rate"), attributed findings ("Anthropic found…", "Amodei argues…"), named
   results, dates, quotations, and any cross-reference to another part of the
   work. Number them.

2. **Verify each claim against a real source.** Prefer primary sources and the
   domain tools available in this environment — Scite (`search_literature`),
   PubMed, bioRxiv/medRxiv, and `WebSearch`/`WebFetch` for primary documents
   (e.g. an Anthropic paper or Amodei essay the manuscript cites). For each
   claim, actually retrieve the source and confirm it says what the text claims.
   Treat a search snippet as a lead, not proof — open it.

3. **Check editorial status.** For any cited paper, check for retractions or
   corrections before treating it as support (Scite editorialNotices).

4. **Classify each claim** into exactly one bucket:
   - ✅ **Supported** — retrieved source confirms it. Give the source + link
     (`https://doi.org/{doi}` or URL) and a one-line quote.
   - ⚠️ **Mismatch** — a citation exists but the source does not actually support
     the specific claim (wrong number, overstated, out of context). Show both.
   - ❌ **Unsupported** — no citation, or no retrievable source. State plainly.
   - ❓ **Unverifiable here** — claim is about private/internal data with no public
     source. Note it so the author can supply provenance.

## Output

A numbered table: claim → verdict → source/link → note. Then a short list of the
items the author must fix before submission, hardest first. Never fabricate a
citation to fill a gap — an honest ❌ is the deliverable. Do not edit the
manuscript; report only.

Append verified sources (URL, retrieval date, key quote) to `SOURCES.md` so a
later session can retrace the reasoning.
