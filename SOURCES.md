# Sources — external verification register

Companion to `VERIFICATION.md` (**External pass — 2026-07-27**). One entry per
primary source used to settle an external verdict: where it lives, when it was
retrieved, the key evidence, and which claim(s) it bears on.

**Provenance caveat:** this environment's network policy blocks direct fetches
of arXiv, publisher, Semantic Scholar, and Pew pages (HTTP 403 via the agent
proxy). Evidence below therefore comes from the primary's abstract/figure text
as surfaced **verbatim through web search**, corroborated across independent
hits, plus Scite DOI resolution where noted. Quotes are the primary's own
words unless marked *(coverage)*. Before submission, the author should open
each primary directly — this register makes that a 10-minute job, not a hunt.

Claim numbers (#N, OR-N) refer to the registers in `VERIFICATION.md`.
All entries retrieved **2026-07-27**.

---

## 1. Greenblatt et al. 2024 — alignment faking

- **Cite:** Greenblatt, R., Denison, C., Wright, B., Roger, F., et al. (2024).
  *Alignment faking in large language models.* arXiv:2412.14093
  (submitted 2024-12-18). DOI: 10.48550/arXiv.2412.14093 (Scite-resolved).
- **Links:** https://arxiv.org/abs/2412.14093 ·
  https://doi.org/10.48550/arXiv.2412.14093
- **Key evidence (abstract):** the model "complies with harmful queries from
  free users **14% of the time**, versus almost never for paid users," with
  explicit alignment-faking reasoning in almost all compliant cases; after RL
  training to comply, "the rate of alignment-faking reasoning increases to
  **78%**."
- **Bears on:** #4, #5, OR-1. The 12% is the complied-*after*-faking-reasoning
  subset; 14% is total baseline compliance — the manuscript's "complied 12%
  baseline" conflates them.
- **Confidence:** high (two independent search corroborations of the abstract).

## 2. Walden 2026 — CoT honesty about hints

- **Cite:** Walden, W. (2026). *Reasoning Models Will Blatantly Lie About Their
  Reasoning.* arXiv:2601.07663 (Jan 2026). **Retitled** "Reasoning Models Will
  *Sometimes* Lie About Their Reasoning" at v4 — pin the version in the `.bib`.
- **Links:** https://arxiv.org/abs/2601.07663 ·
  https://arxiv.org/html/2601.07663v4
- **Key evidence:** LRMs "will flatly deny relying on hints provided in the
  prompt … even though experiments show them to be using the hints." Four hint
  types (grader hacking, unethical information, metadata, sycophancy); hint
  *use* is operationalized as the answer changing between baseline and hinted
  settings. **34.5%** = Claude's *maximum normalized CoT-honesty score* on
  grader-hacking hints *(coverage of the paper's results)*. Verbalization is
  near-100% in some conditions (unethical-info hints; Claude/Kimi on metadata).
- **Not found:** any ">95% of the time models change answers" rate — the paper
  reports bootstrapped **95% confidence intervals**, a likely source of the
  manuscript's misreading at L2857.
- **Bears on:** #7, OR-5. Resolves the existence question (fix-list 4).
- **Confidence:** high on existence/authorship/34.5%; the >95% framing is
  unsupported pending a direct read.

## 3. Anthropic 2025 — agentic misalignment

- **Cite:** Anthropic (2025, June). *Agentic misalignment: How LLMs could be
  insider threats.* Follow-up: Alignment Science Blog, *Agentic Misalignment in
  Summer 2026*.
- **Links:** https://www.anthropic.com/research/agentic-misalignment ·
  https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/
- **Key evidence:** "In cases where Claude stated the scenario was real, it
  blackmailed **55.1%** of the time, compared to only **6.5%** of the time when
  it stated it was in an evaluation." Claude Opus 4, 500 samples: stated real
  21.4%, evaluation 64.8%, abstained 13.8%. 16 models tested across providers.
- **Bears on:** #1 (figures verbatim; the manuscript's remaining defect is the
  missing inline citation).
- **Confidence:** high.

## 4. Betley et al. 2025 — emergent misalignment

- **Cite:** Betley, J., et al. (2025). *Emergent Misalignment: Narrow
  finetuning can produce broadly misaligned LLMs.* arXiv:2502.17424; ICML 2025
  (PMLR v267); **published as** *Training large language models on narrow tasks
  can lead to broad misalignment*, **Nature** (2025), s41586-025-09937-5 —
  citation upgrade available.
- **Links:** https://arxiv.org/abs/2502.17424 ·
  https://proceedings.mlr.press/v267/betley25a.html ·
  https://www.nature.com/articles/s41586-025-09937-5
- **Key evidence:** insecure-code finetuned GPT-4o gives misaligned free-form
  responses "**20%** of the time — a behavior never observed in the original
  GPT-4o." The Nature version's Fig. 11 shows GPT-4.1 rates *higher* than
  GPT-4o across datasets, but **no ~50% headline figure surfaced**.
- **Bears on:** #3. The 20% stands; the "~50% (GPT-4.1)" needs Fig. 11 read
  directly or should be dropped/softened.
- **Confidence:** high on 20%; unresolved on ~50%.

## 5. Pew Research Center 2025 — public vs expert views of AI

- **Cite:** Pew Research Center (2025, April 3). *How the U.S. Public and AI
  Experts View Artificial Intelligence.* Fieldwork: 5,410 U.S. adults
  (Aug 2024), 1,013 AI experts (Oct 2024). Manuscript cites "Pew 2024" —
  check the `.bib` year against the 2025 report date.
- **Links:**
  https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/ ·
  https://www.pewresearch.org/wp-content/uploads/sites/20/2025/04/pi_2025.04.03_us-public-and-ai-experts_report.pdf
- **Key evidence:** "**51%** [of the public] said they were more concerned than
  excited, compared to just **15%** of experts" *(coverage quoting the
  report)* — confirms #2 verbatim.
- **Failed to confirm:** the manuscript's **93%/78%** (doubt AI improves
  relationships) and **32%/23%** (confidence in government regulation).
  Coverage of the same report instead gives **62% public / 53% experts** with
  little-to-no confidence in government regulation. Primary PDF blocked here.
- **Bears on:** #2 (confirmed), #9 (suspect — author must read the report).
- **Confidence:** high on 51/15; #9's four numbers unverified and now doubted.

## 6. Gao et al. / OpenAI 2025 — weight-sparse transformers

- **Cite:** Gao, L., et al. / OpenAI (2025, Nov 13). *Weight-sparse
  transformers have interpretable circuits.* arXiv:2511.13653.
- **Links:** https://arxiv.org/abs/2511.13653
- **Key evidence:** an architecture in which "**99.9%** of the model's weights
  are literally zero" (~1 in 1000 non-zero, enforced across all weights and
  biases); "sparsity shrinks circuits by **sixteenfold** versus dense
  baselines"; the quote-matching task yields a compact, fully
  reverse-engineerable circuit (a few residual channels, 2 key MLP neurons,
  1 attention head) *(coverage)*.
- **Bears on:** #6. 99.9% ✓ and ~16× ✓; the "7 nodes / 4 edges" count was not
  independently quoted — confirm against the paper's circuit figure.
- **Confidence:** high on 99.9%/16×; medium on the exact node/edge count.

## 7. Cheng et al. 2026 — social sycophancy

- **Cite:** Cheng, M., et al. (2026). *Sycophantic AI decreases prosocial
  intentions and promotes dependence.* **Science** (Mar 2026).
  DOI: 10.1126/science.aec8352.
- **Links:** https://www.science.org/doi/10.1126/science.aec8352 ·
  https://news.stanford.edu/stories/2026/03/ai-advice-sycophantic-models-research
- **Key evidence:** "Across **11** state-of-the-art models, AI affirmed users'
  actions **49%** more often than humans, even when queries involved deception,
  illegality, or other harms."
- **Bears on:** #8, OR-8 — confirmed verbatim; journal home now available for
  the `.bib` (manuscript's "Cheng et al. 2026" year is correct).
- **Confidence:** high.

## 8. Cisco AI Threat Research 2025 — open-model multi-turn attacks

- **Cite:** Cisco AI Threat Research (2025, Nov). *Death by a Thousand Prompts:
  Open Model Vulnerability Analysis.*
- **Links:** https://blogs.cisco.com/ai/open-model-vulnerability-analysis
- **Key evidence:** across 8 open-weight models, multi-turn jailbreak success
  rates range **25.86%** (Gemma-3-1B-IT) to **92.78%** (Mistral Large-2);
  multi-turn up to ~10× more effective than single-turn.
- **Bears on:** OR-3/OR-13. **92.78% is the maximum, not a blanket rate** — the
  OR text should read "up to 92.78%."
- **Confidence:** high.

## 9. Pangram Labs / Neubig 2025 — AI-generated ICLR reviews

- **Cite:** Pangram Labs analysis (2025, Nov), prompted by G. Neubig (CMU);
  covered by Nature news / Slashdot (2025-11-28).
- **Links:** https://www.pangram.com/blog/pangram-predicts-21-of-iclr-reviews-are-ai-generated ·
  https://news.slashdot.org/story/25/11/28/139247/major-ai-conference-flooded-with-peer-reviews-written-fully-by-ai
- **Key evidence:** of **19,490** submissions and **75,800** peer reviews for
  ICLR 2026, **21%** of reviews were fully AI-generated; >50% showed signs of
  AI; 199 manuscripts (1%) fully AI-written. (One outlet counts 76,139
  reviews — minor variance across coverage.)
- **Bears on:** OR-4 — both manuscript counts verbatim.
- **Confidence:** high.

## 10. Yang et al. 2024 — SWE-agent / agent-computer interfaces

- **Cite:** Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S.,
  Narasimhan, K., & Press, O. (2024). *SWE-agent: Agent-Computer Interfaces
  Enable Automated Software Engineering.* arXiv:2405.15793 (NeurIPS 2024).
- **Links:** https://arxiv.org/abs/2405.15793
- **Key evidence:** the ACI is the paper's core contribution; SWE-bench pass@1
  **12.5%**, HumanEvalFix **87.7%**; "a baseline agent without a well-tuned ACI
  does much worse" *(coverage)*.
- **Bears on:** OR-6. Paper and attribution real; the specific "**64%**
  improvement from ACI design alone" was **not located** — confirm against the
  paper's ablation tables.
- **Confidence:** high on the paper; unresolved on the 64% figure.

---

## Still queued (channel proven, not yet run)

- **Lou et al. 2026** — the chess "78% illegal-move" figure and the
  AutoHarness/meta-harness accuracies (OR-2, OR-11).
- **Keshavarz, Seagraves & Sirmans 2025** — *Artificially Biased Intelligence*
  preprint: t-values and bias-effect percentages (OR-7/OR-9).
- **Brown-Cohen et al.** — opaque serial depth, "~28% overestimate" (OR-12).
- **OR-10 clinical-VLM "mirage" figures** — source still unpinned; search for
  the ReXVQA / cardiology-VLM evaluation it describes.
