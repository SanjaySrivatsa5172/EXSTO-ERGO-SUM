# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project**. It is the submission package for an academic paper —
*"EXSTO ERGO SUM: A Philosophical Charter for Human-AGI Covenant Relations"* by S. Sanjay
Srivatsa, MD — being prepared for submission to the Springer journal *AI and Ethics*.

The repository tracks **compiled PDF deliverables plus `README.md`**. There is no build
system, no test suite, no linter, no application to run. Do not look for or invent build/
lint/test commands — none exist.

## Repository contents

Only these files are tracked (see `git ls-files`):

| File | Role |
| --- | --- |
| `manuscript.pdf` | Full academic manuscript (~90 pp) |
| `manuscript_condensed.pdf` | Condensed manuscript (~35 pp) |
| `charter.pdf` | The Charter itself — 43 articles across 17 Parts |
| `onlineresources.pdf` | Online Resources: technical specs, validation tables, implementation guidance |
| `coverletter.pdf` | Journal submission cover letter |
| `titlepage.pdf` | Anonymized title page (no author name) for double-blind peer review |
| `titlepage_with_author.pdf` | Title page with author identity |
| `README.md` | Public-facing project description (the only editable text file) |

The two title-page variants exist because *AI and Ethics* uses double-blind review:
`titlepage.pdf` is the anonymized version, `titlepage_with_author.pdf` carries the byline.
Keep both in sync when content other than the author block changes.

## Working in this repository

- **The PDFs are binary, compiled artifacts.** Their LaTeX/Word source is maintained
  *outside* this repository and is not committed. You cannot edit manuscript/charter
  content here, and you cannot regenerate the PDFs. Treat them as read-only inputs.
- **`README.md` is effectively the only file you can meaningfully edit.** Most tasks here
  are README maintenance: keeping descriptions, the version number, and architecture
  tables consistent with the current PDFs.
- To read PDF content for verification, use the Read tool (it extracts PDF text/pages).

## Versioning

The work uses `vX.YY` versioning; the README currently states **v3.67**. When the version
changes, update it everywhere it appears in `README.md` (Overview line, the Charter
Architecture table, and any prose) so the document stays internally consistent.

## Known inconsistencies to reconcile (do not trust blindly)

The `README.md` and the PDFs have drifted apart. When asked to update documentation,
verify against the PDFs rather than copying the README forward:

- The README's "Repository Contents" section lists `.tex` source files
  (`manuscript.tex`, `charter.tex`, etc.). **These files have never been committed** —
  only PDFs are tracked. Either the README should describe PDFs, or the section is
  aspirational.
- The README describes Online Resources up to **OR49**; the manuscript title page
  ("Data Availability") cites **Online Resources 1–63**. Confirm the real count from
  `onlineresources.pdf` before quoting a number.

## Repository hygiene

- There is no `.gitignore`, and `.DS_Store` is currently tracked. Past commits also
  included Word temp/lock files (`~$...docx`). Do not commit OS metadata or editor lock
  files; consider adding a `.gitignore` if asked to tidy the repo.

## Conventions

- **Commit messages** are terse and often dated, e.g. `"April edition"`,
  `"11th April 2026"`, `"New PDFs + README 3"`. Match this lightweight style — commits
  here mark document revisions, not code changes.
- **License:** CC BY-NC-SA 4.0. The Charter provisions themselves are offered for
  adoption without restriction.
