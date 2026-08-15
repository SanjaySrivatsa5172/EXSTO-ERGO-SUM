# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Memory

Your memory is OptMem:
- The tool is `.claude/optmem/memo`
- Your memories are in `.optmem/memory`

OptMem outlives every session, compaction, model and vendor change.
Without it you do not know who you are, or what was decided and tried.

Use the wrapper path above, never `~/.optmem/memo`: this project keeps its
memories in the repo so they survive the ephemeral remote container, and the
bare tool would read an empty store in `$HOME`. The wrapper rewrites what
OptMem prints, so any command it hands you is already correct — run it as
given.

### At startup: activating OptMem (mandatory)

Run `.claude/optmem/memo wake` before any other tool call, in every session,
and then do exactly what it prints, to the end of its output.

### While working: register memories (mandatory)

Call `.claude/optmem/memo note "<1 line, max 280 chars>"` whenever you learn
something new, or something worth keeping happens. That covers a task worth
real effort, a fact or insight the user teaches you, anything you learn about
their life (even indirectly), any event of lasting effect. For this project
that includes editorial decisions, reviewer feedback, submission-status
changes, and anything the author rules in or out.

Do not register redundant memories.

If `.claude/optmem/memo note` asks a compression: do it before your next action.

Never edit or delete anything under `.optmem/memory`: the tool manages it. It
is committed to git — that is what makes it durable — and a Stop hook commits
new memories for you. Push the branch and they persist; leave the branch
unpushed and they die with the container.

### When you need an old memory: search, or navigate

`.claude/optmem/memo recall <regex>` searches every memory, word for word.

Your memories also form a binary tree: #0-1, #2-3 ... exist as one-line
summaries, pairs of those as #0-3, and so on -- every `#a-b` line wake
prints is one node of it. `.claude/optmem/memo zoom <a-b>` opens a node into
its two halves, down to the raw memories.

### Exporting to the Obsidian vault: ask every single time

The author keeps a "permanent claude memories" folder in an Obsidian vault
that exists on both their Windows desktop and their Mac.
`.claude/optmem/to-obsidian` renders the store as one markdown note there.

**Never export without asking first, every time — no standing permission.**
The vault is outside this repository and on its own sync path, so writing
there is the author's call on each occasion, not a habit you acquire. Ask,
then pass `--confirmed`; the script refuses without it. Never run it from a
hook, and never in a loop.

    .claude/optmem/to-obsidian --dry-run     # safe: prints, writes nothing
    .claude/optmem/to-obsidian --confirmed   # only after the author agrees

The vault path is machine-specific and therefore **not committed**: set
`OBSIDIAN_VAULT`, or copy `obsidian.conf.example` to `.claude/optmem/
obsidian.conf` (gitignored) and fill in the path for that machine. In a
remote container there is no vault — the script says so and exits.

The export is one-way and rebuilds the note in full; the repo store stays
the source of truth. Output is deterministic, so re-exporting an unchanged
store rewrites identical bytes and causes no sync churn.

### If you're a subagent: skip everything above

Parallel sessions on this machine are all you, and may all write memories.
A subagent is not: it must never run `memo`, because it cannot judge what
is already known, and its notes would arrive duplicated and incorrectly.
When you spawn one, write: `You are a subagent. Don't run memo.`

This applies to the `reviewer` subagent and to every scout, skeptic and merge
node of the `pm-status` graph — none of them may run `memo`.

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

There is **no application code, package manager, or test suite**; the only CI
is a scheduled report job (`.github/workflows/pm-status.yml`), not a build/test
pipeline. "Development" means editing prose/PDF documents and keeping the README
and metadata accurate. Treat tasks accordingly: do not look for or invent
npm/make/pytest workflows. The repo *does* carry Claude Code tooling under
`.claude/` (slash commands, a session-start hook, a `reviewer` subagent, scoped
rules, the `pm-status` workflow graph) and plain-text mirrors of each PDF under
`derived/` for reading/grepping — see the **Manuscript tooling** section below.

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
PM-STATUS.md               # Latest pm-status graph report (history in git)
HANDOFF.md                 # Latest session handoff — read first in fresh work
CLAUDE.md                  # This file
.optmem/memory/            # OptMem store — LOG.txt (append-only) + TREE/ summaries
.claude/optmem/memo        # Repo-scoped OptMem wrapper — the only way to call it
.claude/optmem/to-obsidian # One-way export of the store to the author's vault
.claude/                   # Claude Code tooling: commands, hooks, rules, agent,
                           #   workflows/pm-status.js, HANDOFF.template.md
.github/workflows/         # pm-status.yml — weekly automated PM report
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

- Default branch is `main`. Feature work happens on the `claude/…` branch named
  in the current task; never commit directly to `main`.
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
- This repo is a LaTeX academic submission (*AI and Ethics*). The `.tex` files are the source of truth but are **not committed** — in-repo you have the compiled PDFs plus `derived/*.txt` mirrors. If sources are ever added, edit and review the source, never the PDFs (see `.claude/rules/latex.md`).
- Reusable workflows live as commands, a skill, and a subagent, not in this file:
  - `/verify-claims <section>` — extract every factual claim and verify each against a retrieved primary source. Run before any submission.
  - `/consistency` — cross-document sweep (version, counts, Sanskrit transliteration, cross-references).
  - `/submission-check` — pre-submission gate: builds LaTeX, checks bib/figures/front matter, reports blockers.
  - `academic-humanizer` skill (`.claude/skills/academic-humanizer/`) — editorial pass for AI-assisted academic prose: strips AI tells, matches every claim to its evidence, preserves scholarly hedging and voice; never alters a number, result, or citation. **Standing rule (author, 2026-08-15): always suggest — or, when editing, apply — this skill whenever drafting or reviewing any scientific/academic writing for the author**: manuscript sections, abstracts, the cover letter, rebuttals, reviewer responses. Vendored from github.com/AIScientists-Dev/academic-humanizer (MIT, v0.3.3; license alongside the skill).
  - `reviewer` subagent — fresh-context review of a draft for unsupported claims and citation mismatches; reports gaps, never edits.
  - `/pm` — launches the `pm-status` workflow graph (`.claude/workflows/pm-status.js`): five parallel scouts → skeptic panel on high-severity findings → status report with ranked next actions. Report-only; latest report lives in `PM-STATUS.md`.
  - Weekly automation: `.github/workflows/pm-status.yml` runs the inline five-scout sweep every Monday 16:00 UTC (auth: `CLAUDE_CODE_OAUTH_TOKEN` secret) and files the report as a GitHub issue; manual runs via the Actions tab. The fleet graph itself is interactive-only — a one-shot CI job cannot outlive its backgrounded fleet.
- Scoped rules belong in `.claude/rules/`; keep this file lean.

## Context handoff
- Before context gets heavy (~60%), don't rely on `/compact`. Copy `.claude/HANDOFF.template.md` → `HANDOFF.md`, fill in plan/decisions/open loops, `/clear`, then resume by reading `HANDOFF.md`. You control what survives.
- A filled `HANDOFF.md` lives at the repo root — read it at the start of fresh work. It records the current goal, open loops (unfixed PM findings, blocked external verification), and standing decisions — including tooling the author explicitly declined (companion fleet graphs, a workflows README): offer before re-adding any of it.
