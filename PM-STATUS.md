# PM-STATUS — project-manager graph report

**Run date:** 2026-07-21 · **Produced by:** the `pm-status` workflow graph
(`.claude/workflows/pm-status.js`, launched via `/pm`) · **Run:**
`wf_918f593f-42c` — 30 agents (5 scouts, 24 panel skeptics, 1 synthesis),
0 errors, ~23 min · **Verification model:** every high-severity finding below
survived a three-lens adversarial panel (reproduce / severity / staleness,
≥2 of 3 votes); watchlist items are scout-reported and **unverified by the
panel**.

This file holds the latest report; prior reports live in git history. Two
watchlist items were already resolved the same day by the tooling session
that ran the graph: the uncommitted `pm-status.js` change (committed as
`699c628`) and the unmerged tooling branch (merged as PR #10, `3ef3d5f`).

---

# EXSTO ERGO SUM — project status

**Overall state: needs attention** — deliverables are intact and internally versioned, but the submission front-matter contradicts itself and the external citation-verification layer remains almost entirely undone.

## State of the project

All seven deliverable PDFs are present at the repository root with matching `derived/*.txt` mirrors, and the core version facts — Charter v3.67, 43 articles, 17 Parts, five pillars (Pañca-Stambha) — agree across README, charter, and both manuscripts. The main documents, however, are not yet submission-coherent: the cover letter addresses the wrong journal, the "anonymized" title page names the author, and the Online Resources count differs across four documents. Inside `onlineresources.pdf`, stale v3.66 self-references and an outdated Zero–XXXVI numbering note contradict the current v3.67 charter. Verification debt is substantial: the internal audit layer is complete for the manuscript and Online Resources, but the external layer (reading primary sources) is ~0% done, with 20+ verdicts blocked and load-bearing figures (Walden 2026, the 78% alignment-faking statistic, the OR-10 clinical VLM figures) still unconfirmed. The `.claude/` tooling is largely healthy, with modest documentation drift, and the working tree carries one uncommitted change on the tooling branch.

## Confirmed risks

All eight high-severity findings survived panel review; none were refuted.

1. **Wrong journal in the cover letter.** The letter is addressed to *Minds and Machines* (derived/coverletter.txt:10-16, :179 "Fit with Minds and Machines"), while README.md:172 and :234 and CLAUDE.md name *AI and Ethics*. A cover letter naming the wrong journal is an immediate desk-reject embarrassment.
2. **The anonymized title page is not anonymized.** derived/titlepage.txt:7-11 names "Dr Sanjay Srivatsa" as author and corresponding author, defeating double-blind review.
3. **Online Resources count disagrees across documents.** README.md:108-116 ends at OR49; derived/titlepage_with_author.txt:61 says "Online Resources 1–58"; derived/titlepage.txt:56 and derived/coverletter.txt:17 say "1–63"; the cover letter also says "ORs 38–58" (:72) and names an "OR58" enclosure file (:230).
4. **Stale v3.66 self-identification inside the Online Resources.** derived/onlineresources.txt:97 and :7231 ("Online Resource 31: Charter v3.66 Technical Specification"), plus :7503, :9134, :10379, :10981, versus v3.67 references at :14457, :14583, :15197 and README.md:24.
5. **Article-numbering note is out of date.** derived/onlineresources.txt:11651 states contiguous numbering runs "Zero–XXXVI" under v3.66, but README.md:22 and derived/charter.txt:1759/:2035 confirm Zero–XXXVII (43 articles) under v3.67.
6. **External verification layer entirely blocked.** VERIFICATION.md:14-19, 25-33, 67-84, 118-123: every external verdict except #10 (Amodei) is PRIMARY READ BLOCKED by network/MCP tool-approval failure; four items are explicitly queued (Pew 2024, Betley 2025, Greenblatt 2024, Walden 2026). No primary source has been read for any load-bearing empirical figure.
7. **The "confabulated reasoning" evidence rests on an unverified reference.** "Walden (2026)" [59] (>95% / <34.5% CoT figures) has unconfirmed existence and attribution, with inconsistent OR-5 phrasing (VERIFICATION.md:31, 49-51, 71, 94).
8. **The 78% figure remains mislabeled in the manuscript and OR.** "Strategic compliance" should read "alignment-faking reasoning after RL" at manuscript L2083 and OR L7071/L7186/L10500; only the README was fixed, and a second unrelated 78% (chess illegal-move rate) invites conflation in OR §51.2 (VERIFICATION.md:29, 37-42, 67-68, 88-93, 102-106).

## Watchlist

Medium and low findings, unverified by the panel:

- **Medium** — Neither manuscript states the current Charter version; manuscript.txt:2109 discusses only the 3.55→3.60 evolution, which could read as current-version 3.60.
- **Medium** — Internal component stamps "Online Resources v3.46" and "Charter SDK v3.53" (onlineresources.txt:1813, :1827) may need bumping to v3.67.
- **Medium** — Uncited/mis-cited claims remain: #1 (55.1%/6.5%) uncited at point of claim, #3 first-mention citation absent, #4 baseline possibly 14% not 12% (VERIFICATION.md:25-28, 47-53).
- **Medium** — OR-10 clinical VLM figures (>60%, 90–100%, 33–38.5%, ReXVQA 10%) have no located source (VERIFICATION.md:81, 99-100, 116-117).
- **Medium** — charter.pdf, coverletter.pdf, and both title pages have never been swept by any verification pass; no SOURCES.md exists.
- **Medium** — OR-14 risk: the <0.1% throughput / <1% FNR figures are design-targets, not measured results; the distinguishing fix is not yet applied (VERIFICATION.md:85, 95-98).
- **Medium** — Author affiliation varies: "Independent Scholar" (author title page, cover letter), "Independent Researcher" (anonymized title page), "Director, Heart Artery and Vein Center" (README.md:191-196).
- **Medium** — Cover letter carries an unresolved arXiv ID placeholder (coverletter.txt:195-196).
- **Medium** — Cover letter is internally inconsistent on the OpenClaw incident date: February 2026 (:46) vs January 2026 (:99-100).
- **Medium** — Uncommitted change to .claude/workflows/pm-status.js on branch claude/graph-engineering-pm-ptnlmy. *(Resolved same day: committed as 699c628.)*
- **Medium** — CLAUDE.md's Manuscript tooling section omits the /pm command and pm-status workflow present on disk. *(Resolved same day: documented in CLAUDE.md.)*
- **Medium** — /consistency, /submission-check, and .claude/rules/latex.md assume `.tex` sources that are not committed, so those commands cannot run as written.
- **Low** — Verification run is ~4 weeks old (2026-06-25); README L62 "Anthropic's own empirical findings" framing was flagged but left to the author.
- **Low** — Both title pages omit the "EXSTO ERGO SUM:" title prefix that the README citation includes.
- **Low** — License statements (CC BY-NC-SA repo, MIT SDK, unrestricted Charter adoption) do not conflict but could use a one-line clarification in README.
- **Low** — onlineresources.txt references a "Proposed Amendment toward Charter v3.68 — Vikāsa-Maryādā" companion document not present in the repo (:19409, :19443, :19810).
- **Low** — CLAUDE.md is internally contradictory about whether PDFs or .tex are the source of truth.
- **Low** — settings.json MCP allowlist entries (mcp__Scite_mcp, mcp__PubMed, mcp__bioRxiv) do not match the UUID-based server identifiers active in this environment and are likely inert.
- **Low** — Tooling branch work (pm-status workflow, commit 1fb7702) is unmerged to main; no HANDOFF.md or SOURCES.md exists; hook wiring and command frontmatter verified healthy; all PDFs and mirrors present with matching timestamps. *(Branch merged same day as PR #10.)*

## Discarded by the panel

None — the skeptic panel confirmed all eight high-severity findings; no finding was refuted.

## Next actions

1. Decide the actual target journal and align the cover letter (coverletter.tex → coverletter.pdf), README.md citation block, and CLAUDE.md so every document names the same venue.
2. Regenerate the anonymized title page (titlepage.tex → titlepage.pdf) with all author-identifying information removed, or drop the anonymized designation if the journal is single-blind.
3. Establish the true Online Resources count from onlineresources.pdf and make README.md, titlepage.pdf, titlepage_with_author.pdf, and every mention in coverletter.pdf agree.
4. Unblock the scholarly MCP/network channel and complete the external primary-source pass on all PRIMARY READ BLOCKED and queued items in VERIFICATION.md, starting with Walden 2026 [59], Greenblatt 2024, Betley 2025, and Pew 2024.
5. Propagate the 78% "alignment-faking reasoning after RL" relabel into the external manuscript and onlineresources .tex sources and disambiguate the second 78% chess statistic in OR §51.2.
6. Update the stale v3.66 references and the Zero–XXXVI numbering note in the onlineresources .tex source to v3.67 / Zero–XXXVII and rebuild onlineresources.pdf.
7. Locate and pin the OR-10 clinical VLM source in onlineresources.pdf, or remove/reframe those figures if no source exists.
8. Run an internal-layer verification sweep over charter.pdf and coverletter.pdf and create SOURCES.md to record every source, retrieval date, and key quote.
9. Fix the remaining cover letter defects in coverletter.pdf — one affiliation string, a resolved or future-tense arXiv ID, and a single consistent OpenClaw incident date.
10. Reconcile CLAUDE.md's tooling section with disk (add /pm and pm-status, resolve the .tex-vs-PDF source-of-truth contradiction) and commit or discard the pending .claude/workflows/pm-status.js change.
