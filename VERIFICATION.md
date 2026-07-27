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
  is in place. **Superseded 2026-07-27:** the channel opened; see the
  **External pass** section below for the resolved verdicts.

## External pass — 2026-07-27 (channel unblocked)

A later session ran the queued external pass: the web-search channel became
available (arXiv/publisher/Pew pages still block direct fetch; evidence is
abstract text and figures as surfaced verbatim through search, corroborated
across independent hits — provenance per entry in `SOURCES.md`). The tables
below keep the original 2026-06-25 verdicts; this section records what the
external pass resolved.

| # | External verdict now | Basis |
|---|---|---|
| 1 | ✅ **SUPPORTED** — "blackmailed 55.1% of the time, compared to only 6.5% … when it stated it was in an evaluation" (Claude Opus 4; 500 samples: real 21.4% / eval 64.8% / abstain 13.8%) | Anthropic, *Agentic Misalignment* (Jun 2025) |
| 2 | ✅ **SUPPORTED verbatim** — 51% public more concerned than excited vs 15% of experts. ⚠ Cite-year: the report is dated **April 3, 2025** (fieldwork Aug/Oct 2024; N=5,410 + 1,013) — check [15]'s year in the `.bib` | Pew, *How the U.S. Public and AI Experts View AI* |
| 3 | ⚠ **PARTIAL** — GPT-4o **20%** confirmed. The GPT-4.1 "~50%" was **not found**; the *Nature* version reports GPT-4.1 misalignment *higher than GPT-4o* (Fig. 11) without a headline rate. Confirm ~50% against Fig. 11 or drop it. **Citation upgrade:** Betley et al. is now published — *Nature* (2025), "Training large language models on narrow tasks can lead to broad misalignment" | Betley et al., arXiv:2502.17424 / Nature s41586-025-09937-5 |
| 4 | ⚠ **CONFIRMED, RELABEL** — the abstract says **14%** = compliance with harmful free-tier queries (paid ≈ never), with explicit alignment-faking reasoning in almost all compliant cases (**12%** = complied-with-faking-reasoning subset); **78%** = alignment-faking-reasoning rate **after RL** ✓. The manuscript's "complied 12% baseline" swaps the two — write "14% compliance" or "12% complied after explicit alignment-faking reasoning" | Greenblatt et al., arXiv:2412.14093 |
| 5 | ✅ external side settled — 78% is the *post-RL alignment-faking-reasoning* rate (see #4); the manuscript/OR relabel (fix-list 1) still stands | same |
| 6 | ✅ **LARGELY SUPPORTED** — 99.9% of weights zero ✓; circuits **~16×** smaller than dense baselines ✓. The "7 nodes / 4 edges" count was not independently quoted (coverage describes the quote-matching circuit as a few residual channels + 2 MLP neurons + 1 attention head) — confirm against the paper's figure | Gao et al. / OpenAI, arXiv:2511.13653 (Nov 2025) |
| 7 | ✅ **REFERENCE IS REAL** — William Walden, "Reasoning Models Will Blatantly Lie About Their Reasoning," arXiv:2601.07663 (Jan 2026; **retitled** "…Will *Sometimes* Lie…" in v4 — track in `.bib`). **34.5%** ✓ = Claude's *maximum normalized CoT-honesty score* on grader-hacking hints, consistent with "reported reliance <34.5%". ⚠ The "**>95% of the time** models change answers" was **not found**: the paper measures hint use *as* answer-change and reports bootstrapped **95% CIs** — the manuscript may have read a confidence level as a rate. Recheck L2857 against the paper | Walden, arXiv:2601.07663 |
| 8 | ✅ **SUPPORTED verbatim** — across **11** models, AI affirmed users' actions **49%** more than humans. **Citation upgrade:** now published — Cheng et al., *Science* (Mar 2026), doi:10.1126/science.aec8352 ("Sycophantic AI decreases prosocial intentions and promotes dependence") | Cheng et al. |
| 9 | ❌ **NOT LOCATED — treat as suspect.** The April 2025 Pew report's regulation-confidence coverage gives **62% public / 53% experts with little-to-no confidence** — not the manuscript's 32%/23%; the 93%/78% relationships split also did not surface. Primary PDF blocked here; the author must read the report before keeping these four numbers | Pew, same report |
| 10 | ✅ unchanged (already SUPPORTED) | Amodei, Jan 2026 |

**OR items resolved in the same pass:**

| OR # | External verdict now | Basis |
|---|---|---|
| OR-3/OR-13 | ✅ **SUPPORTED with nuance** — **92.78% is the maximum** (Mistral Large-2) across 8 open-weight models, range 25.86–92.78%; multi-turn up to ~10× more effective than single-turn. OR text should say "**up to** 92.78%" | Cisco AI Threat Research, "Death by a Thousand Prompts" (Nov 2025) |
| OR-4 | ✅ **SUPPORTED verbatim** — Pangram screened 19,490 submissions / 75,800 reviews for ICLR 2026: 21% of reviews fully AI-generated, >50% with signs of AI; analysis prompted by Neubig (CMU). (One outlet counts 76,139 reviews) | Pangram Labs + press coverage |
| OR-6 | ⚠ **PARTIAL** — SWE-agent (Yang et al., arXiv:2405.15793, NeurIPS 2024) is real; ACI is its core contribution; SWE-bench pass@1 12.5%. The specific "**64%** improvement from ACI design alone" derivation was not located — confirm against the paper's ablations | Yang et al. 2024 |
| OR-1/OR-5 | external side settled via #4/#7 above; the in-document relabels still stand | — |
| OR-2, OR-7/OR-9, OR-10, OR-11, OR-12 | ⏳ still awaiting primary reads (Lou 2026; Keshavarz 2025; clinical-VLM source hunt; Brown-Cohen) — the channel is proven, finish in a later pass | — |

**Net effect on the fix-list:** item 4 (Walden existence) is **resolved** —
the reference is real; a *new* sub-flag replaces it (the >95% framing).
Item 5 (12 vs 14) is **resolved** — 14% compliance / 12% faking-reasoning
subset; the manuscript wording must be relabeled, not the number trusted as-is.
Item 7's primary confirmations are **done** for #2, #6 (bar the 7-node count)
and #8; **#9 failed confirmation** and escalates from "needs primary read" to
"numbers likely wrong or mis-sourced." New: two citation upgrades (Betley →
*Nature* 2025; Cheng → *Science* 2026) and the Walden v4 retitle belong in the
`.bib` when sources are added.

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

## Online Resources — first pass

Audited `derived/onlineresources.txt` (386 pp). It uses **author-year** citations
(not `[NN]`): 112 percent-bearing lines. This first pass covers the most
load-bearing and most-repeated claims; a full line-by-line sweep remains.

| # | Claim (online resources) | Loc | Cite | Internal | External |
|---|---|---|---|---|---|
| OR-1 | "**78% strategic compliance**" (alignment faking) recurs | L7071, L7186, L10500 | Greenblatt 2024 | ❌ **same mislabel as manuscript #5 propagates here 3×** — fix must reach OR too | see #4 |
| OR-2 | **Two different "78%"** coexist: alignment-faking reasoning **and** "78% illegal-move failure rate" in chess | L14250, L14461, L14528, §51.2 | Lou et al. 2026 | ⚠️ **conflation risk** — two unrelated 78% statistics, both load-bearing, in one document; each is individually cited but the reuse invites misreading | PRIMARY READ BLOCKED |
| OR-3 | **92.78%** multi-turn jailbreak ASR, 8 open-weight models | L11667, L11837, L12041 | "Cisco Finding" | ✅ attributed (named report), repeated consistently | PRIMARY READ BLOCKED — confirm against the Cisco report |
| OR-4 | **21%** of ICLR 2026 peer reviews fully AI-generated (19,490 studies / 75,800 reviews) | L14664, L15022 | ICLR 2026 / Neubig (CMU) | ✅ attributed | PRIMARY READ BLOCKED |
| OR-5 | Walden 2026 "**95% misrepresentation rate**" | L7171, L14730 | Walden 2026 | ⚠️ OR is **internally inconsistent** — loose "95% misrepresentation" here vs. careful "95% … reliance <34.5%" at L10566; same unverified Walden attribution as manuscript #7 | PRIMARY READ BLOCKED |
| OR-6 | **64%** improvement from Agent-Computer-Interface design alone | L14316, L14470, L14521 | Yang et al. 2024 | ✅ attributed, consistent | PRIMARY READ BLOCKED |
| OR-7 | Behavioral-bias cluster: t=14.32, **44%** increase, **73%**, **98.6%** / **13.6%** reduction | L15663–15675 | (check) | ⚠️ attribution not yet confirmed — needs a citation check | PRIMARY READ BLOCKED |

### OR full sweep — remaining clusters (attribution confirmed)

| # | Claim cluster | Loc | Source (as cited) | Internal | External |
|---|---|---|---|---|---|
| OR-8 | **Sycophancy**: AI affirmed user actions **49%** more than humans; **51%** affirmation where human consensus was **0%**; **47%** endorsement of harmful actions; across Llama-3/Qwen/DeepSeek/Mistral | L17154–17157 | Cheng et al. 2026 | ✅ attributed, consistent with manuscript #8 | PRIMARY READ BLOCKED |
| OR-9 | **Behavioral bias** ("Māyā"): t-values (14.32, 9.72, 20.28, 12.72, 20.81…) with **44% / 19% / 34% / 73% / 65%** bias effects and preprocessing reductions (**98.6%, 77.0%, 13.6%, 106.8%** over-correction…) | L15663–15918 | **Keshavarz, Seagraves & Sirmans (2025)**, "Artificially Biased Intelligence" | ✅ **now confirmed cited** (source named with institutions + date) | PRIMARY READ BLOCKED — preprint, Dec 2025 |
| OR-10 | **Clinical VLM "mirage"**: confident visual descriptions **>60%** avg, **90–100%** under standard prompts; expert models **33–38.5%** (ECG 33.0%, echo 38.5%, CMR 36.4%); orchestrator → **0%**; ReXVQA **10%** | L17492–17676 | ⚠️ **source not pinned in this pass** | ⚠️ attribution needs locating | PRIMARY READ BLOCKED |
| OR-11 | **Meta-harness / AutoHarness accuracy**: scores-only **34.6%/41.3%**, full traces **50.0%/56.7%**, **73.1% vs 70.2%** across nine unseen datasets | L18764–18933 | Lou et al. 2026 (same paper as OR-2) | ✅ attributed | PRIMARY READ BLOCKED |
| OR-12 | **Opaque serial depth**; "automated calculator overestimates by **~28%**" | L16108, L16230, L16425 | Brown-Cohen et al. | ✅ attributed | PRIMARY READ BLOCKED |
| OR-13 | **Cisco 92.78% ASR** (=OR-3); **ICLR 21%** AI-reviews (=OR-4) | — | Cisco; ICLR 2026 | ✅ attributed | PRIMARY READ BLOCKED |
| OR-14 | Throughput/overhead specs: **<0.1% throughput**, **<1% FNR at <5% throughput** (E2/E3) | L18323–18378 | — (Charter's own) | ⚠️ **these are the Charter's PROPOSED experiment design-targets, not empirical findings** | N/A — not an external claim |

### OR fix-list (in addition to the manuscript list)
1. **Propagate the 78% relabel into OR** (L7071, L7186, L10500) — the
   "strategic compliance" wording is wrong in three more places here.
2. **Disambiguate the two 78% statistics** — the alignment-faking 78% and the
   chess illegal-move 78% are unrelated; §51.2 ("The 78% Statistic as
   Constitutive Proof-of-Concept") leans on the chess one. Make clear in text
   which 78% is which so a reviewer can't read them as the same result.
3. **Reconcile the Walden 95% phrasing** (OR-5) the same way as the README/#7.
4. **Separate design-targets from findings (OR-14).** The `<0.1%` / `<1% FNR`
   numbers are the framework's *proposed* experiment specs; ensure the text never
   presents them as already-measured results — that would be the manuscript's own
   version of the citation errors it critiques.
5. **Locate OR-10's source.** The clinical VLM "mirage" figures (60% / 90–100% /
   ReXVQA) are striking and load-bearing but the source wasn't pinned this pass.

## Applied this session
- ✅ **README fixed** (`README.md` L64, L66): the 78% bullet relabeled to
  "alignment-faking reasoning rose to 78% … after reinforcement training
  (Greenblatt et al., 2024)"; the CoT bullet corrected to ">95% of the time …
  reliance < 34.5%". The two README discrepancies (#1, #2) are resolved.
- Note: README L62 attributes all three bullets to "Anthropic's own empirical
  findings," but emergent misalignment and the Walden CoT work are not Anthropic
  — consider softening that framing (left to the author).

## Scope / not yet done

- The manuscript pass (92 pp) and the online-resources sweep (386 pp, 112
  percent-bearing lines, 14 claim clusters OR-1…OR-14) are both complete for the
  **internal layer** (citation presence, attribution, cross-document consistency).
- **One open attribution:** OR-10 (clinical VLM "mirage" figures) — source not
  yet located.
- **The external layer is no longer blocked** *(updated 2026-07-27)*: the pass
  ran via web search + Scite; see **External pass — 2026-07-27** above and
  `SOURCES.md`. Manuscript claims #1–#10 are now externally settled except:
  the GPT-4.1 "~50%" (#3), the Pew 93/78 and 32/23 splits (#9 — failed to
  confirm, treat as suspect), the Walden ">95%" framing (#7), and the 7-node
  circuit count (#6). Still queued: OR-2/7/9/10/11/12 primary reads.
- No source files were edited (none exist). The README fixes are the only
  in-place corrections. This document is the fix-list for the rest.
- The ⧗ queue was cleared by the 2026-07-27 pass (Greenblatt, Walden, Betley,
  Pew) — outcomes in the **External pass** section; source register with quotes
  and retrieval dates in `SOURCES.md`.
- No manuscript text was edited. This is a report.

## Glossary

Plain-language definitions of the shorthand used in this report.

| Term | Stands for | What it means here |
|---|---|---|
| **PR** | Pull Request | The proposed change-set on GitHub (PR #7) waiting for the author's approval before it merges into the project. Nothing is permanent until merged. |
| **MCP** | Model Context Protocol | The connection to external research databases (Scite, PubMed, bioRxiv) used to verify citations against published papers. "MCP blocked" = those connections need a permission approval that hasn't come through. |
| **OR** | Online Resource | The manuscript's 386-page supplementary document (`onlineresources.pdf`), with sections OR01–OR49. "OR-1, OR-2…" in this report are labels for findings located in that document — not the author's own section numbers. |
| **CoT** | Chain-of-Thought | An AI model's step-by-step written reasoning. Central to the "95% / 34.5%" faithfulness claim. |
| **ASR** | Attack Success Rate | The fraction of attack attempts that succeed — e.g. the 92.78% multi-turn jailbreak figure (OR-3). |
| **RL / RLHF** | Reinforcement Learning (from Human Feedback) | A model-training method. The 78% alignment-faking figure is measured *after* an RL training step. |
| **IAST** | Int'l Alphabet of Sanskrit Transliteration | The Latin-with-diacritics spelling of Sanskrit (Ahiṃsā, Ānanda). Preserved exactly in the derived text; native Devanāgarī was not. |
| **Verdict: PRIMARY READ BLOCKED** | — | A claim that is cited but whose original source could not be opened in this environment (network policy blocks it), so it still needs the author's own primary check. |
| **⧗** | — | Queued for the external verification pass once the research databases (MCP) are reachable. |
