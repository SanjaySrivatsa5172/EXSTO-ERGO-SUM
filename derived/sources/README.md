# Captured sources

Full text of web sources retrieved for claim and citation verification, written
here by `tools/source_capture.py`. The index of what is in this directory —
title, URL, retrieval date, excerpt — is `SOURCES.md` at the repository root.

## Status: reference, NOT source

The same rule that governs `derived/*.txt` governs these files. They are
**machine-extracted page text**: a lossy view of the page as it stood on the
retrieval date recorded in each file. The publisher's version is authoritative.

A capture is evidence that a URL was retrieved on a given date and what it said
at that moment. It is *not* a primary read. Before quoting a source in the
manuscript, open the publisher's page.

## What will be missing

| Aspect | Fidelity |
|---|---|
| Body prose, headings, list items, block quotations | ✅ Extracted |
| `<title>`, `description`, Open Graph metadata | ✅ Extracted |
| Diacritics and non-ASCII text (Ahiṃsā, Ānanda…) | ✅ Preserved — UTF-8 throughout, tested |
| JavaScript-rendered content | ❌ **Lost** — the fetch is static HTML only; the tool warns when a page yields almost nothing |
| Paywalled or bot-walled body text | ❌ Usually lost; metadata may still confirm the citation exists |
| PDFs and other binaries | ❌ Not captured — the tool refuses them rather than writing an empty file |
| Figures, tables, math | ❌ Flattened or dropped |

## Why these are committed

Sessions run in ephemeral containers with restricted egress, so a page read in
one session is unavailable in the next. Committing the capture is what lets a
later session — or a reviewer, or the author months from now — retrace a
verification without re-fetching anything.

## Add a capture

```bash
python3 tools/source_capture.py <url>
```

Do not add or edit files here by hand; re-run the tool instead, which also keeps
`SOURCES.md` in step. See `tools/README.md` for the safety model and the
network-policy caveats.
