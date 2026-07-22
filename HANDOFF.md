# Session handoff — 2026-07-21

Read this before doing anything else in a fresh session on this repository.
It records the graph-engineering session that built the PM tooling, ran it,
and merged it.

## Where we are
- Working branch: `claude/graph-engineering-pm-ptnlmy`, restarted from `main`
  before each follow-up per the merged-PR rule; tooling history runs through
  PR #18 (`main` at `f8d6fb5`), first automated report filed as Issue #19.
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
- [x] Weekly routine live as a repo-native GitHub Actions schedule:
  `.github/workflows/pm-status.yml` (Mondays 16:00 UTC). Auth is the
  `CLAUDE_CODE_OAUTH_TOKEN` secret (author's Claude subscription, via
  `claude setup-token`); the stored `ANTHROPIC_API_KEY` has no API credits
  and its input is disabled in the workflow — do not re-enable without
  adding credits first.
- [x] First authenticated run validated (run #7, 2026-07-21: ~5½ min,
  $2.17 on claude-sonnet-5, full report produced). It exposed two headless
  gaps — the Workflow tool and gh needed interactive approval — fixed by
  `--dangerously-skip-permissions` in claude_args and by moving issue
  filing into a deterministic workflow step (Claude writes
  /tmp/pm-report.md; plain `gh issue create` files it). Run #8 exposed a
  third: the Workflow tool backgrounds its fleet and the one-shot job
  exits before it finishes, so the CI prompt now mandates the inline
  five-scout sweep; the fleet graph stays interactive-only via /pm.
- [ ] Author works through the next actions in `PM-STATUS.md` and the latest
  weekly issue (currently #19, ten items). Most require the external `.tex`
  sources (the repo ships PDFs only); the exceptions — SOURCES.md creation
  and tooling-doc reconciliation — can be done in-repo.

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
- **Scheduling is repo-native (GitHub Actions), not a claude.ai Routine** —
  the remote-session trigger API was declined twice at the approval prompt,
  so the routine lives as `.github/workflows/pm-status.yml`: durable,
  reviewable in git, and account-independent. A desktop or
  claude.ai/code/routines routine remains a valid alternative the author can
  add from their own UI; do not create one via the trigger API unprompted.
- **`PM-STATUS.md` keeps a stable filename** (latest report in place, history
  in git), matching the `VERIFICATION.md` convention.

## Open loops / unresolved
- **End-to-end issue delivery pending one green run.** After the delivery
  fix, one manual dispatch (Actions tab → "Weekly PM status" → Run
  workflow) should end with an issue titled "PM status — <date>"; confirm
  it appears, then the loop is fully closed. On-demand alternatives: `/pm`
  in any session on this repo, or the same Actions button anytime.
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
- Merged history: PR #10 `3ef3d5f` (graph + /pm) · #11 `581e851` (artifacts)
  · #12 `909c1e8` (Actions routine) · #13 `105c1ce` (CI auth) · #14 `d0c2f9c`
  (model pin + output) · #15 `696d00f` (subscription-token auth) · #16
  `6d6a85c` (session PM pulse) · #17 `e1940d7` (deterministic issue filing)
  · #18 `f8d6fb5` (inline sweep mandate). First automated report: Issue #19.

## Next action
- Confirm one post-fix run files its issue (see Open loops). Then the real
  work: PM-STATUS Next action 1 — pick the target journal and align cover
  letter, README citation, and CLAUDE.md; the un-anonymized title page is
  the other desk-reject-class fix.
