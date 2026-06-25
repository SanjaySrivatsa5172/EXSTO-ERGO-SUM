---
description: Conventions for the LaTeX manuscript sources
globs: ["*.tex", "*.bib"]
---

# LaTeX manuscript rules

- The `.tex` and `.bib` files are the source of truth. The `.pdf` files
  (manuscript, charter, online resources, etc.) are build artifacts — never
  hand-edit a PDF; change the `.tex` and rebuild.
- Preserve Sanskrit diacritics exactly (Ahiṃsā, Saṃskāra-Vyākaraṇa,
  Sat-Cit-Ānanda, Pañca-Stambha). Do not silently ASCII-fold them.
- Keep cross-references symbolic (`\ref`, `\cite`, `\label`) — never hard-code a
  number a reference could resolve to, so renumbering stays safe.
- Don't introduce a new citation without a matching `.bib` entry, and verify the
  source supports the claim (see `/verify-claims`) before adding it.
- After any source change, rebuild and confirm zero undefined references and zero
  missing citations before calling it done.
