---
description: Cross-document consistency sweep across the manuscript, charter, online resources, cover letter, and README — version strings, counts, terminology, transliteration, and cross-references.
argument-hint: optional — a single file to check against the rest, else checks all
---

You are running a consistency sweep across this manuscript set
($ARGUMENTS if given, otherwise: manuscript.tex, manuscript_condensed.tex,
charter.tex, onlineresources.tex, coverletter.tex, titlepage.tex, README.md).

A multi-file submission drifts: the version bumps in one file but not another,
an article count changes, a Sanskrit term is spelled two ways. Reviewers notice.
Find the drift before they do.

## Step 0 — run the mechanical checker first

Before reasoning by hand, run the deterministic signal generator:

```bash
python3 .claude/consistency/check.py
```

It scans `derived/*.txt` + `README.md` and reports, with verified `file:line`
evidence, the *distribution* of version strings, counts, Sanskrit
transliterations, and Online-Resource cross-references — flagging the minority,
out-of-band, and ASCII-folded cases. It is a **signal, not a verdict**: it never
demands uniformity (a changelog legitimately names old versions; a proposal
names a future one), so every flag is a candidate you must judge in context.
Use its output as the spine of the checks below — it will not miss a version
token or a folded diacritic the way a hand-sweep can, and it frees you to spend
judgement on whether each flagged item is real drift or intentional. When the
script and your own reading disagree, reconcile the difference explicitly rather
than trusting either blindly. (The script reads only the plain-text mirrors; if
`.tex` sources are ever added, confirm the same values there too.)

## Then check, with the file:line evidence for each mismatch

1. **Version string** — every stated version agrees (currently v3.67). Flag any
   stale number.
2. **Counts** — article count (43, Zero–XXXVII), Part count (17), pillar count
   (5, Pañca-Stambha). Confirm they match wherever stated, and that an enumerated
   list actually contains that many items.
3. **Terminology & transliteration** — Sanskrit terms are spelled and diacritically
   marked consistently (e.g. Ahiṃsā, Saṃskāra-Vyākaraṇa, Sat-Cit-Ānanda). Flag
   divergent spellings and missing/!inconsistent diacritics.
4. **The five pillars** — Karma, Dharma, Ahiṃsā, Viveka, Ānanda appear as the
   same set with the same Sanskrit/Devanāgarī wherever listed.
5. **Cross-references resolve** — every "Online Resource N", "Article X", "Part Y",
   "Table Z" points to something that exists and is numbered as stated. Flag
   dangling or misnumbered references.
6. **Author/metadata** — name, ORCID, affiliation, journal, citation block match
   across README, titlepage, and coverletter.

## Output

A grouped list of mismatches, each with the conflicting `file:line` values and
the value you believe is correct (with reasoning). End with a one-line verdict:
consistent, or N issues to resolve. Do not edit — report only, so the author
decides the canonical value.
