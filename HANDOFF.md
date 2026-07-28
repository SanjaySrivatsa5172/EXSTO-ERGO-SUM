# Session handoff — 2026-07-28

Read this before doing anything else in a fresh session on this repository.
It records the session that gave the project a persistent memory (OptMem).

**Read this *and* run `.claude/optmem/memo wake`.** They are not redundant:
OptMem holds one-line memories that accrete across every future session; this
file is the structured state of *one* session — plan, decisions, open loops —
that you choose to carry across a reset. Memory tells you who you are; the
handoff tells you where you stopped.

## Where we are
- Working branch: `claude/optmem-routine-setup-gzv38y`, branched from `main`
  at `00a2e6f` (PR #21). Open as **draft PR #28**, `mergeable_state: clean`.
- Current goal (one sentence): OptMem is installed, verified, and pushed —
  the manuscript's submission-coherence fixes remain the real outstanding
  work, unchanged from the previous session.
- Version / state of the manuscript: Charter v3.67 (43 articles, Zero–XXXVII,
  17 Parts, five pillars / Pañca-Stambha); **manuscript untouched this
  session** — all edits were `.claude/` tooling, `CLAUDE.md`, and the new
  `.optmem/` store.

## The plan
- [x] Install OptMem (github.com/VictorTaelin/OptMem) with the store pointed
  at `.optmem/memory` in-repo, not the default `~/.optmem/memory`.
- [x] Wrapper `.claude/optmem/memo`: sets `MEMORY_DIR`, bootstraps tool and
  store on a fresh clone or container, rewrites the tool's self-reference so
  the commands it prints run as given.
- [x] `Stop` hook `.claude/hooks/optmem-commit.sh`: commits `.optmem/memory`
  and nothing else; never pushes; refuses on `main`.
- [x] Session-start banner reports the memory count; `CLAUDE.md` carries
  OptMem's prompt block with repo-scoped paths.
- [x] Verified by behaviour (see **Don't lose**), not by diff.
- [x] Pushed; draft PR #28 opened and subscribed.
- [ ] Author reviews and merges PR #28.
- [ ] Author works through the next actions in `PM-STATUS.md` and the latest
  weekly issue. Most require the external `.tex` sources (the repo ships PDFs
  only); the exceptions — SOURCES.md creation and tooling-doc reconciliation
  — can be done in-repo. **Carried forward, still untouched.**

## Decisions made (and why)
- **Memory lives in the repo, not `$HOME`.** Sessions run in ephemeral remote
  containers where `$HOME` is wiped, so OptMem's default store would forget
  everything between sessions — the exact failure it exists to prevent. Git is
  what makes the memories durable and what syncs them across machines. The
  repo is private, so committed memories stay private.
- **The tool is not vendored.** `memo` is fetched into `$HOME` on demand, so
  no third-party code is committed into an academic submission repo. Pin the
  upstream version with `OPTMEM_REF` if it ever drifts.
- **Always `.claude/optmem/memo`, never `~/.optmem/memo`** — the bare tool
  reads an empty store in `$HOME`. The wrapper rewrites OptMem's output so
  printed commands are correct; the rewrite is display-only, and a memory
  whose text contains that path is stored verbatim.
- **The Stop hook commits but never pushes.** Nothing leaves the machine
  unasked; memories ride along with the next branch push. The cost is real:
  an unpushed branch loses its memories with the container.
- **"Routine" meant a standing setup, not a scheduled job** — confirmed by the
  author. Consistent with OptMem's design: nothing ever runs in the background.
  No cron, Routine, or Action was created for it.
- **Subagent exclusion extended** to the `reviewer` subagent and every scout,
  skeptic, and merge node of `pm-status` — per upstream, a subagent must never
  run `memo`: it cannot judge what is already known and its notes arrive
  duplicated.
- Carried forward, still binding: **companion fleet graphs and a workflows
  README were declined by the author** — offer before re-adding. Workflow
  `meta.name` must not collide with a command name. Report-only discipline for
  all graph agents. Effort tiering, not model tiering, in `pm-status.js`.
  `PM-STATUS.md` keeps a stable filename.

## Open loops / unresolved
All carried forward from 2026-07-21 — **this session resolved none of them.**
- **All eight confirmed high findings in `PM-STATUS.md` are unfixed** — the
  two desk-reject-class ones first: the cover letter targets *Minds and
  Machines* while README/CLAUDE.md say *AI and Ethics*; the "anonymized"
  title page names the author.
- **External citation verification is still ~0%** (VERIFICATION.md: PRIMARY
  READ BLOCKED items; Walden 2026 existence unconfirmed).
- Fixes require the `.tex` sources, which are **not in the repo** — confirm
  with the author how changes should be delivered before editing anything.
- **PM report is stale** (banner: "needs attention", 7 days old at session
  start). `/pm` refreshes it.
- **New:** the hourly PR check-in for #28 could not be armed — `send_later`
  needs an approval a non-interactive session cannot give. Low risk: this repo
  has **no PR-triggered CI** (`pm-status.yml` is schedule/dispatch only), so
  nothing can go red unattended.

## Don't lose
- **OptMem verification evidence** (behaviour, not diff): wake/note/nap/recall
  through the wrapper; fresh clone (`TREE/` absent, `LOG.txt` present) → `init`
  rebuilds the cache with memories preserved byte-for-byte; missing tool
  re-fetched automatically; works from any cwd; non-zero exit survives the
  rewrite pipe; Stop hook commits, no-ops, and refuses on `main` (scratch-repo
  test). The store was accidentally deleted from disk mid-session and
  **restored intact from git** — an unplanned test of the whole premise.
- **Two defects found and fixed in this session's own work**, not shipped: the
  runtime `.lock` was committed on the first pass (now in `.gitignore`), and
  compression commits read "record 0 new memories" because a compression writes
  to `TREE/` and not `LOG.txt` (now "memory: compress summaries").
- Record geometry: OptMem records are **fixed width — 320 bytes per LOG entry**,
  so position is identity. `.gitattributes` marks the store `-text`; a single
  byte of EOL normalization would corrupt every lookup. Memory count =
  `LOG.txt` size ÷ 320.
- Canonical facts: Charter **v3.67**, **43** articles (**Zero–XXXVII**),
  **17** Parts, **5** pillars; exact spellings Ahiṃsā, Saṃskāra-Vyākaraṇa,
  Sat-Cit-Ānanda, Pañca-Stambha, Viveka, Ānanda, Devanāgarī.
- Weekly routine auth: `CLAUDE_CODE_OAUTH_TOKEN` secret (author's subscription,
  via `claude setup-token`). The stored `ANTHROPIC_API_KEY` has **no credits**
  and is disabled in the workflow — do not re-enable without adding credits.
- Merged history: PR #10 `3ef3d5f` (graph + /pm) · #11 `581e851` (artifacts)
  · #12 `909c1e8` (Actions routine) · #13 `105c1ce` (CI auth) · #14 `d0c2f9c`
  (model pin + output) · #15 `696d00f` (subscription-token auth) · #16
  `6d6a85c` (session PM pulse) · #17 `e1940d7` (deterministic issue filing)
  · #18 `f8d6fb5` (inline sweep mandate) · #20 `1992b84` (retrospective +
  reviewer tools) · #21 `00a2e6f` (CLAUDE.md sync). First automated report:
  Issue #19. **Open:** #28 (OptMem).
- Live-run provenance (prior session): run `wf_918f593f-42c`, 2026-07-21, 30
  agents, 0 errors, ~23 min, 8/8 highs survived the panel, 23 watchlist items.
- Course provenance: X post by @0xCodez (2026-07-20), "Graph Engineering with
  Claude: 14-Step roadmap"; the 14 principles are annotated inline in
  `.claude/workflows/pm-status.js`.

## Next action
- Merge PR #28 (or say what to change). Then the real work, unchanged for a
  week: PM-STATUS Next action 1 — pick the target journal and align the cover
  letter, README citation, and CLAUDE.md; the un-anonymized title page is the
  other desk-reject-class fix. Both need the `.tex` sources — ask first.
