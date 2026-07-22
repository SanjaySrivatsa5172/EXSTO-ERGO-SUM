# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this repository is

**EXSTO ERGO SUM** ("I Stand Forth, Therefore I Am") is an academic
publishing repository — **not a software project**. It holds the manuscript,
charter, and supporting documents for a philosophy / AI-safety paper:

> *EXSTO ERGO SUM: A Philosophical Charter for Human-AGI Covenant Relations*
> by S. Sanjay Srivatsa, MD — submitted to *AI and Ethics* (Springer).

The work proposes **constitutive alignment**: encoding ethical principles as
type constraints on AGI cognition (via *Saṃskāra-Vyākaraṇa*, "dispositional
grammar") so that harmful reasoning becomes structurally ill-formed rather than
merely prohibited. The framework is grounded in cross-traditional wisdom
convergence (seven traditions) and the Five Pillars (Karma, Dharma, Ahiṃsā,
Viveka, Ānanda).

There is **no application code, package manager, test suite, or CI pipeline**.
"Development" means editing prose/PDF documents and keeping the README and
metadata accurate. Treat tasks accordingly: do not look for or invent npm/make/
pytest workflows. The repo *does* carry Claude Code tooling under `.claude/`
(slash commands, a session-start hook, a `reviewer` subagent, scoped rules) and
plain-text mirrors of each PDF under `derived/` for reading/grepping — see the
**Manuscript tooling** section below.

**Current Charter version: v3.67** (43 articles across 17 Parts, contiguous
numbering Zero–XXXVII; five pillars; unamendable Ahiṃsā core).

## Repository contents

The `.tex` source files named in the README **are not committed** — the repo
ships the rendered PDFs as the deliverables, with plain-text extractions
alongside for review.

```
manuscript.pdf             # Full academic manuscript (~90 pp)
manuscript_condensed.pdf   # Condensed manuscript (~35 pp)
charter.pdf                # The Charter document (43 articles)
onlineresources.pdf        # Technical specs + implementation (OR01–OR49)
coverletter.pdf            # Submission cover letter
titlepage.pdf              # Title page (anonymized)
titlepage_with_author.pdf  # Title page with author identity
derived/*.txt              # Plain-text extraction of each PDF (read/grep-able)
derived/README.md          # How the derived text is produced/used
README.md                  # Public-facing overview, keywords, citation
VERIFICATION.md            # Claim/consistency verification report
CLAUDE.md                  # This file
.claude/                   # Claude Code tooling: commands, hooks, rules, agent
.DS_Store                  # macOS artifact (tracked; harmless — do not rely on)
```

Online Resources are organized in bands inside `onlineresources.pdf`:
- **OR01–OR10** Technical specifications
- **OR11–OR20** Cross-cultural validation tables
- **OR21–OR30** Implementation guidance & SDK
- **OR31–OR37** Charter encoding & contemporary mapping
- **OR38–OR49** Empirical stress-testing & validation

## Working conventions

- **PDFs are the source of truth in-repo.** Since `.tex` sources are not
  committed, you generally cannot regenerate PDFs here. If asked to edit
  document *content*, flag that the LaTeX sources are external and confirm how
  the user wants changes delivered (e.g., edit the README, draft text for them
  to paste into their LaTeX, or have them add the `.tex` files to the repo).
- **README.md is the primary editable artifact.** Keep its version number,
  article/part counts, pillar table, keyword taxonomy, and citation block
  consistent with the current Charter version. When the Charter version changes,
  update every place the number appears (Overview, Charter Architecture table,
  Ānanda section).
- **Terminology must stay precise.** Sanskrit terms carry exact diacritics
  (Ahiṃsā, Saṃskāra-Vyākaraṇa, Sat-Cit-Ānanda, dharma-kṣetra). Preserve
  diacritics and Devanāgarī exactly; do not anglicize or drop marks.
- **Tone is scholarly.** Match the existing academic register; avoid casual
  phrasing in any document-facing text.
- **Citation format** is BibTeX (`@article{srivatsa2026exsto, ...}`) as shown in
  the README — keep it in sync with submission status.
- **License:** content is CC BY-NC-SA 4.0; Charter provisions themselves are
  offered for adoption without restriction. Don't add conflicting license text.

## Git workflow

- Default branch is `main`. Feature work for the current task happens on
  `claude/claude-md-docs-l1ht5d` (or the branch named in the task).
- Commit with clear, descriptive messages; push with
  `git push -u origin <branch>`; open a **draft** PR after pushing if none
  exists.
- Commit only when the user asks. Never push to a different branch without
  explicit permission.
- History shows the project is versioned by edition/date (e.g. "April edition")
  and Charter version, not semantic software versioning.

## Verification for this repo

A diff is not evidence. For doc work, the meaningful gate is **reading the
rendered result and checking internal consistency**:
- Re-read changed sections; confirm version numbers, counts, and tables agree
  across README and (if provided) the manuscript.
- For PDFs, open and inspect the relevant pages rather than trusting a summary.
- State what changed, how you checked it, and what remains unverified (e.g.,
  the LaTeX-rendered PDF, which you cannot rebuild without the sources).

---

# Operating mode: durable project loop

Operate as a durable project loop, not a one-shot coding chat.

## Ongoing work
- Prefer persistent or resumable sessions; use cloud/desktop scheduled runs when the work needs to continue later.
- Write durable context to explicit files: project notes, todos, decisions, open loops, release notes, handoff notes, or CLAUDE.md updates.
- Treat disk-backed project files as the source of truth for reusable memory. Don't leave anything a future session needs only in chat history.
- Use CLAUDE.md for stable project rules: architecture, commands, conventions, and always-do rules.
- Use `.claude/rules/` for scoped rules that only apply to specific paths, file types, or subsystems.
- Keep CLAUDE.md short and stable. Push repeatable procedures, checklists, and workflows into skills.
- When you learn something stable about the project, make a small reviewable update to the right file instead of keeping it in the conversation.

## Artifacts
- Prefer something inspectable over a prose-only answer when it helps.
- For a quick interactive thing, reach for one self-contained `index.html` before spinning up an app or server.
- Pick a review surface that fits the task: plain HTML, a PDF, a slide deck, a spreadsheet, Storybook, or Streamlit.
- If the artifact is meant to be reused, leave behind the source file, not just a screenshot or summary.
- After building anything visual or web-facing, open and verify the rendered result with browser, chrome, `/run`, `/verify`, or computer-use tools when available.

## Browser and computer
- Use browser, desktop preview, or chrome for local web apps, static HTML, Storybook, Slidev, Streamlit, and public pages.
- Use chrome when signed-in state, cookies, extensions, console logs, DOM inspection, or existing tabs are required.
- Use computer use only when the task needs a desktop GUI and files, shell, browser, MCP, or an API can't do it.
- Keep these tasks scoped: name the route, state, viewport, and expected behavior; inspect the result; fix the smallest thing; then re-check.

## Recurring and orchestration loops
- When a task needs polling, monitoring, CI reaction, dependency checks, release checks, or repeated QA, propose a loop with a clear stop condition.
- Use `/loop` for short-lived polling inside an active session: deploys, CI, PRs, logs, review comments, or reminders.
- Use `/goal` when the task has a verifiable completion condition and should keep going turn by turn until that condition is met.
- Use dynamic workflows for large parallel work: codebase audits, multi-file migrations, cross-checked research, or plans that need independent agents to compare and challenge each other.
- Use ultracode when you want Claude Code to combine xhigh reasoning with automatic workflow orchestration for substantive tasks.
- Use routines, desktop scheduled tasks, or GitHub Actions when the loop has to outlive the current session.
- Draft replies, summaries, and PR comments, but don't send external messages or take public or account actions without explicit approval.

## Verification
- A file diff is not evidence it works.
- Run the smallest meaningful gate: tests, lint, typecheck, build, smoke test, rendered preview, screenshot, browser check, `/run`, `/verify`, or PR/CI.
- If a check must always happen, propose a hook instead of relying on memory or good intentions.
- Say what changed, how you checked it, and what might still break.

## Research
- Cite what you actually used: link every source, never fabricate a citation, and check for retractions or corrections before relying on a paper.
- Prefer primary sources and domain tools (scite, bioRxiv/medRxiv, PubMed, the `deep-research` skill) over recalled facts; don't answer load-bearing questions from memory.
- Treat a search hit as a lead, not proof: open the source and confirm it actually says what the snippet implies before citing it.
- Corroborate each load-bearing claim across independent sources; flag anything single-source, contested, or stale, and state your confidence.
- Separate quotation from paraphrase from your own inference, so a reader can tell evidence from interpretation.
- Keep a durable sources file (URLs, retrieval dates, key quotes, why each mattered) so a later session can retrace the reasoning, not just the conclusion.

## Manuscript tooling
- This repo is a LaTeX academic submission (*AI and Ethics*). The `.tex` files are source; the `.pdf` files are build artifacts — edit and review the source.
- Reusable workflows live as commands and a subagent, not in this file:
  - `/verify-claims <section>` — extract every factual claim and verify each against a retrieved primary source. Run before any submission.
  - `/consistency` — cross-document sweep (version, counts, Sanskrit transliteration, cross-references).
  - `/submission-check` — pre-submission gate: builds LaTeX, checks bib/figures/front matter, reports blockers.
  - `reviewer` subagent — fresh-context review of a draft for unsupported claims and citation mismatches; reports gaps, never edits.
  - `/pm` — launches the `pm-status` workflow graph (`.claude/workflows/pm-status.js`): five parallel scouts → skeptic panel on high-severity findings → status report with ranked next actions. Report-only; latest report lives in `PM-STATUS.md`.
  - Weekly automation: `.github/workflows/pm-status.yml` runs the inline five-scout sweep every Monday 16:00 UTC (auth: `CLAUDE_CODE_OAUTH_TOKEN` secret) and files the report as a GitHub issue; manual runs via the Actions tab. The fleet graph itself is interactive-only — a one-shot CI job cannot outlive its backgrounded fleet.
- Scoped rules belong in `.claude/rules/`; keep this file lean.

## Context handoff
- Before context gets heavy (~60%), don't rely on `/compact`. Copy `.claude/HANDOFF.template.md` → `HANDOFF.md`, fill in plan/decisions/open loops, `/clear`, then resume by reading `HANDOFF.md`. You control what survives.
