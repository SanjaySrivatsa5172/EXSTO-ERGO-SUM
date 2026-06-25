# Derived text (extracted from PDFs)

These `.txt` files are **machine-extracted** from the compiled PDFs with
`pdftotext -layout -enc UTF-8` on 2026-06-25. They exist so the manuscript's
prose can be read, searched, and run through `/verify-claims` and `/consistency`
inside a session — the original `.tex` sources are not in this repo.

## Status: reference, NOT source

Per `.claude/rules/latex.md`, the source of truth is `.tex`/`.bib`. The PDFs are
build artifacts; **these `.txt` files are a lossy derivative of the artifacts.**
Do not treat them as editable source and do not "rebuild" from them.

## What survived, what didn't

| Aspect | Fidelity |
|---|---|
| English prose | ✅ Clean and complete |
| Latin/IAST Sanskrit diacritics (Ahiṃsā, Saṃskāra-Vyākaraṇa, Ānanda, māyā…) | ✅ Preserved exactly — verified, zero ASCII-folding |
| Native Devanāgarī (कर्म, धर्म, अहिंसा…) | ❌ **Lost** — the embedded script font has no recoverable Unicode map; pdftotext drops it. Affects the Devanāgarī column in Charter pillar tables. |
| Inline math symbols (→ ∈ ≤ etc.) | ⚠️ Mostly survive |
| LaTeX math structure (fractions, subscripts, alignment) | ❌ Flattened/mangled — read the PDF for equations |
| Tables | ⚠️ Reading order preserved; column structure approximate |
| `\ref`/`\cite`/`\label` markup | ❌ Resolved to printed numbers; symbolic structure gone |

## Regenerate

```
for f in titlepage titlepage_with_author coverletter charter \
         manuscript manuscript_condensed onlineresources; do
  pdftotext -layout -enc UTF-8 "$f.pdf" "derived/$f.txt"
done
```

To recover Devanāgarī or exact equations you need the original `.tex`, or an OCR
pass with a Sanskrit/Devanāgarī language model — neither is done here.
