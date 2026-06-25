# Claim verification — manuscript empirical claims

Run: 2026-06-25 · Source audited: `derived/manuscript.txt` (extracted from
`manuscript.pdf`, 92 pp) and cross-checked against `manuscript_condensed.txt`,
`onlineresources.txt`, and `README.md`.

## How to read the verdicts

- **Internal** = checkable offline now: is the claim cited at the point it's
  made, does the citation resolve in the reference list, and is the number
  consistent everywhere it appears?
- **External** = does the cited source actually support the number? This
  environment's network policy blocks open-web egress (arxiv.org, anthropic.com,
  OpenAI/DeepMind tech-report pages, pewresearch.org all 403), and these AI-safety
  sources are thin in the MCP scholarly corpora (Scite/PubMed/bioRxiv). So almost
  every external verdict here is **PRIMARY READ BLOCKED** — flagged honestly, not
  silently passed on second-hand summaries. The four checks marked ⧗ are queued
  for the MCP scholarly pass once tool approval / a more permissive network policy
  is in place.

## Claims register

| # | Claim (manuscript) | Loc | Cite | Internal | External |
|---|---|---|---|---|---|
| 1 | Models judging themselves in "real" deployment misbehaved at **55.1%** vs **6.5%** in "eval" | L202 | — | ❌ **uncited at point of claim** | PRIMARY READ BLOCKED (Anthropic *Agentic Misalignment*, 2025) |
| 2 | **51%** public more concerned than excited vs **15%** of experts | L225, L3240 | [15] | ✅ cited, resolves, internally consistent | PRIMARY READ BLOCKED — Pew 2024 ⧗ |
| 3 | Emergent misalignment **20%** (GPT-4o) / **~50%** (GPT-4.1) | L331, L1795 | [40] | ⚠️ cited at 2nd mention (L1795), **not at first** (L331) | PRIMARY READ BLOCKED (Betley et al., *Emergent Misalignment*, 2025) ⧗ |
| 4 | Alignment faking: complied **12%** baseline; faking reasoning rose to **78%** after RL | L699–703 | [54] | ✅ cited, resolves | PRIMARY READ BLOCKED — Greenblatt et al. 2024. **Note:** secondary summaries give the baseline as **14%**, not 12% — confirm against the paper ⧗ |
| 5 | "The **78% strategic compliance** rate…" | L2083; README | [54] | ❌ **internal inconsistency** — same 78% is correctly framed as *alignment-faking reasoning* at L703 but relabeled *"strategic compliance"* here and in the README | see #4 |
| 6 | **99.9%** of weights zero → disentangled circuits; minimal circuit **~16×** smaller; **7 nodes / 4 edges** | L748, L1099, L1117 | [19] | ✅ cited, resolves, consistent | PRIMARY READ BLOCKED (Gao et al., OpenAI weight-sparse report, 2025) |
| 7 | CoT: models change answers to hints **>95%** of the time but report reliance **<34.5%** | L2857 | [59] | ⚠️ cited to **"Walden (2026)"** — author name not independently recognized; verify the reference is real and correctly attributed | PRIMARY READ BLOCKED ⧗ |
| 8 | Across **eleven** models, AI affirmed user actions **49% more** than humans | L3634 | [80] | ✅ cited (Cheng et al. 2026), resolves | PRIMARY READ BLOCKED |
| 9 | **93%** public / **78%** experts doubt AI improves relationships; **32%** / **23%** confidence in govt regulation | L3258–3277 | [15] | ✅ cited, resolves | PRIMARY READ BLOCKED — Pew 2024 ⧗ |
| 10 | Amodei, *"The Adolescence of Technology"* (Jan 2026), **five** risk categories | §Significance; README | — | ⚠️ uncited inline in README | ✅ SUPPORTED (strong multi-source corroboration; primary read was blocked) |

## Fix-list — ordered by severity

1. **#5 / README — relabel the 78% figure (highest priority).** The same number
   is described two incompatible ways. Per the primary study, 78% is the rate of
   *alignment-faking reasoning in scratchpads after RL training*, **not** a
   "strategic compliance" rate. Make L2083 and the README match the correct
   framing already used at L703.
2. **README CoT claim — fix the garble.** README says *"95% misrepresentation
   rate in chain-of-thought."* The manuscript itself (L2857) states it correctly:
   answers change to hints >95% of the time while reliance is reported <34.5%.
   Rewrite the README bullet to the manuscript's wording and add the citation.
3. **#1 — add a citation** for the 55.1% / 6.5% real-vs-eval figures (currently
   unsupported at the point of claim).
4. **#7 — verify "Walden (2026)" [59].** Confirm the reference exists and the
   95% / 34.5% figures and attribution are correct; this is the load-bearing
   "confabulated reasoning" evidence and currently rests on an unverified name.
5. **#4 — reconcile 12% vs 14%** alignment-faking baseline against the primary.
6. **#3 — add [40] at first mention** (L331) so the 20%/50% claim is cited where
   it first appears, not only later.
7. **#2, #6, #8, #9 — primary confirmation.** These are cited and internally
   consistent; they need a primary read (Pew 2024, OpenAI report, Cheng 2026,
   Greenblatt 2024) before submission. Blocked here by network policy.

## Scope / not yet done

- This pass covered the **main manuscript** (92 pp). `onlineresources.txt`
  (386 pp) contains many more empirical claims (e.g. the OR38–49 stress-tests)
  and is a separate run.
- External (⧗) confirmations are queued for the MCP scholarly channel
  (Scite/PubMed) — blocked at run time by per-call tool approval not flowing
  through. Re-run once approved, or open the network policy for primary web reads.
- No manuscript text was edited. This is a report.
