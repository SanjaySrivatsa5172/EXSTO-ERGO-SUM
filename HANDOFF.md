# Session handoff — 2026-07-21

Read this before doing anything else in a fresh session on this repository.
It records the graph-engineering session that built the PM tooling, ran it,
and merged it.

## Where we are
- Working branch: `claude/graph-engineering-pm-ptnlmy` (restarted from `main`
  after PR #10 merged as `3ef3d5f`).
- Current goal (one sentence): the project-manager graph is built, verified,
  and merged; the manuscript itself now needs the submission-coherence fixes
  the graph confirmed.
- Version / state of the manuscript: Charter v3.67 (43 articles, Zero–XXXVII,
  17 Parts, five pillars / Pañca-Stambha); manuscript untouched this session —
  all edits were `.claude/` tooling and project docs.

## The plan
- [x] Read the "Graph Engineering with Claude" 14-step course (scan + clean
  X-post text by @0xCodez) and construct it for this repo.
- [x] Build `.claude/workflows/pm-status.js` (scope → fan out → reduce →
  verify → synthesize) and the `/pm` command.
- [x] Fix the scout-attribution defect (names attached before null-filter).
- [x] Validate with a live fleet run: `wf_918f593f-42c`, 30 agents, 0 errors.
- [x] Merge to `main` (PR #10, squash `3ef3d5f`); PR watch closed.
- [x] Save the run's report to `PM-STATUS.md`; document `/pm` in CLAUDE.md.
- [ ] Author creates the weekly routine (see Open loops — paste-ready block).
- [ ] Author works through `PM-STATUS.md` Next actions 1–9 (all require the
  external `.tex` sources; the repo ships PDFs only).

## Decisions made (and why)
- **Only the PM graph shipped.** Companion graphs (claims-verification fleet,
  consistency fleet, error sweep, research scan) and a workflows README were
  drafted but **declined by the author at write time** — do not re-add them
  unprompted; offer first.
- **Workflow names must not collide with command names** — a workflow's
  `meta.name` registers alongside slash commands, so `verify-claims` is
  unavailable as a workflow name (taken by the command). Use e.g.
  `verify-claims-fleet` if that graph is ever wanted.
- **Report-only discipline for all graph agents** (no repo writes), matching
  `/verify-claims`, `/consistency`, and the `reviewer` subagent — the author
  is the only writer in this repo.
- **Effort tiering instead of model tiering** in `pm-status.js` (scouts low,
  synthesis high): the Workflow API advises inheriting the session model
  unless confident; effort is the finer lever here.
- **Weekly cadence, Mondays 9:00 AM Pacific** chosen for the routine — author
  commits are authored at UTC-07:00.
- **Scheduling was not armed from the remote session** — the trigger call
  requires an approval the author declined; the author will create the
  routine themselves (desktop or claude.ai/code/routines).
- **`PM-STATUS.md` keeps a stable filename** (latest report in place, history
  in git), matching the `VERIFICATION.md` convention.

## Open loops / unresolved
- **The weekly routine is not yet created.** Paste-ready instruction block:

  ```
  Run the weekly project-status pulse for EXSTO ERGO SUM. Invoke the /pm
  command (the pm-status workflow graph in .claude/workflows/). If /pm is
  unavailable, fetch branch claude/graph-engineering-pm-ptnlmy and launch the
  Workflow tool with scriptPath .claude/workflows/pm-status.js — this is my
  explicit request to run that workflow. Present the returned report in full,
  dated, leading with confirmed high-severity findings; note in one line if
  nothing changed since last week. Report-only: change, commit, and push
  nothing. Preserve Sanskrit diacritics exactly (Ahiṃsā, Saṃskāra-Vyākaraṇa,
  Sat-Cit-Ānanda, Pañca-Stambha).
  ```

  Desktop: Routines → New routine → Local, weekly Mon 9:00 AM, folder = the
  local clone. Cloud: https://claude.ai/code/routines, repo
  SanjaySrivatsa5172/EXSTO-ERGO-SUM, cron `0 16 * * 1` (UTC).
- **All eight confirmed high findings in `PM-STATUS.md` are unfixed** — the
  two desk-reject-class ones first: cover letter targets *Minds and Machines*
  while README/CLAUDE.md say *AI and Ethics*; the "anonymized" title page
  names the author.
- **External citation verification is still ~0%** (VERIFICATION.md: PRIMARY
  READ BLOCKED items; Walden 2026 existence unconfirmed).
- Fixes require the `.tex` sources, which are **not in the repo** — confirm
  with the author how changes should be delivered before editing anything.

## Don't lose
- Live-run provenance: run `wf_918f593f-42c`, 2026-07-21, 30 agents
  (5 scouts + 24 skeptics + 1 synthesis), 0 errors, ~23 min, 8/8 highs
  survived the panel, 23 watchlist items.
- Canonical facts: Charter **v3.67**, **43** articles (**Zero–XXXVII**),
  **17** Parts, **5** pillars; exact spellings Ahiṃsā, Saṃskāra-Vyākaraṇa,
  Sat-Cit-Ānanda, Pañca-Stambha, Viveka, Ānanda, Devanāgarī.
- Course provenance: X post by @0xCodez (2026-07-20), "Graph Engineering with
  Claude: 14-Step roadmap"; the 14 principles are annotated inline as
  comments in `.claude/workflows/pm-status.js`.
- Merged history: PR #10 → squash `3ef3d5f` (tooling), prior commits
  `1fb7702` (graph + command), `699c628` (attribution fix).

## Next action
- Author: create the weekly routine (block above). First working session
  after that: PM-STATUS Next action 1 — pick the target journal and align
  cover letter, README citation, and CLAUDE.md.
