# Research & Analysis Playbook — *EXSTO ERGO SUM*

A working set of **analytical** prompts and standing instructions for using an
AI collaborator (long-context model) to interrogate, stress-test, and strengthen
the manuscript toward peer review at *AI and Ethics* and similar venues.

Scope: this playbook concerns **deep research and synthesis** — the reasoning
that has to be right *before* the prose matters. (The rhetorical /
content-production prompts are deliberately out of scope.) It adapts a general
synthesis-prompt library into a form fit for **scholarly writing**, and
specifically for *this* manuscript, which fuses empirical AI-safety findings,
philosophical argument, and cross-traditional (esp. Vedantic) framing.

The orientation is opinionated on purpose: scholarly analysis optimizes for
*calibrated truth and defensibility under hostile review* — not persuasion.

---

## How to use this

Two modes:

1. **Paste-in prompts.** Copy a prompt, attach the relevant documents
   (`manuscript.pdf`, `onlineresources.pdf`, `charter.pdf`, or a target
   section), and run it.
2. **Standing rubric.** The final section can be given once at the start of a
   session as persistent instructions for how the AI should reason about your
   work.

A note on context: these prompts are designed to reason across *everything at
once* — the 90-page manuscript, the 49 Online Resources, and the charter
together. Run them on the full corpus, not one file at a time; the value is in
the cross-document patterns a single-file read cannot see.

---

## Why the analytical prompts transfer to scholarship (and the rhetorical ones don't)

Deep-synthesis prompts are, in effect, **a pre-submission peer review you run on
yourself.** Steelmanning the opposition, separating *what we know / think we know
/ are guessing*, isolating the load-bearing assumption, flagging
correlation-as-causation — these are precisely the lenses a referee brings. Run
them on your own work first and you neutralize the rejection before it is written.

For *this* manuscript there is a sharper reason. Its originality — empirical
findings + philosophy + devotional Sanskrit framing — is also its largest
reviewer risk: a referee at an ethics journal may read the *Sat-Cit-Ānanda*
framing as advocacy rather than analysis. Analytical prompts that test the
*argument* (rather than dress it up) are exactly what keep the work legible as
scholarship.

---

## Tier A — Core synthesis prompts (use as-is)

These survive translation to academic writing unchanged.

**A1. Calibrated-claims audit**
> Read the manuscript and the Online Resources. Produce a table that labels
> every substantive claim as one of: *established* (well-supported by cited
> evidence), *plausible* (argued but not demonstrated), or *speculative*
> (conceptual proposal). Flag any claim whose stated confidence exceeds its
> support.

**A2. Load-bearing assumption**
> Identify the single assumption that, if a reviewer rejected it, would
> invalidate the most downstream claims. Explain exactly why it is load-bearing,
> and where in the text it is currently defended (or merely asserted).

**A3. Steelman the rejection**
> You are a skeptical referee for *AI and Ethics* who is unconvinced that ethical
> principles can be encoded as "type constraints" rather than behavioral rules.
> Write the strongest possible report arguing for rejection, using only the
> manuscript's own claims and evidence. Then list what the manuscript would need
> to add to neutralize each objection.

**A4. Correlation / causation & overclaim hunt**
> List every place where the manuscript states something as established fact that
> is actually an assumption, an analogy, or a correlation presented as causation.
> Cite each instance by section.

**A5. Empirical-citation hygiene**
> Extract every empirical or numerical claim (e.g., "78% strategic compliance,"
> "95% misrepresentation rate") with its source and date. For each, assess
> whether the manuscript's use of the figure matches what the source actually
> reported, flag any stated more strongly than the source supports, and flag any
> that may be stale.

**A6. Gap analysis for the rebuttal**
> Tell me what a thorough reviewer will still want that isn't here. Rank the gaps
> by how likely each is to be raised in review, and note which are fixable before
> resubmission versus which require new work.

**A7. Honest one-paragraph summary test**
> Write the most honest one-paragraph summary of what this manuscript actually
> establishes — no framing, no advocacy. Then tell me where the abstract claims
> more than that paragraph supports.

**A8. Agreement / contradiction / silence map**
> Across the full corpus, identify the three claims all the cited sources agree
> on, the three they contradict each other on, and the single most important
> thing none of them address. Locate each in the source material.

**A9. Consensus / minority / fringe placement**
> For the central thesis, identify where it sits relative to the field: what is
> mainstream AI-safety consensus, what is a defensible minority position, and
> what a reviewer will read as fringe. Be specific about which of the
> manuscript's claims fall in each band.

**A10. Underlying-disagreement map**
> Map the real disagreement between this framework and Constitutional AI — not
> the surface dispute, but the underlying disagreement about definitions,
> methodology, or values driving it. State the crux a reader must resolve to
> choose between them.

---

## Tier B — Built for *this* manuscript's specific risks

These target the failure modes most likely for an interdisciplinary,
philosophically-framed AI-safety paper.

**B1. The jargon load budget.**
> Inventory every specialized term (Sanskrit and technical: *Saṃskāra-Vyākaraṇa*,
> *dharma-kṣetra*, "Level 2 gap," "type constraints," etc.). For each, note
> whether it is defined on first use and whether it earns its place. A reviewer
> forced to hold 30 undefined coinages in working memory turns hostile.
> Recommend which terms to keep, gloss, or retire.

**B2. The two-audience translation test.**
> This paper must satisfy two referees at once: a technical AI-safety reader and
> a philosophy/ethics reader. Identify passages that read as under-rigorous to
> the technical reader, and (usually different) passages that read as
> under-rigorous to the philosophy reader.

**B3. Analogy-vs-mechanism audit.**
> The central move is that ethics can be encoded as a "grammar" making harmful
> reasoning "ill-formed." Identify every point where this is asserted as
> *analogy* versus specified as *mechanism*. Reviewers press hardest where a
> compelling metaphor stands in for a missing mechanism. List the spots that need
> mechanism, not metaphor.

**B4. Advocacy-vs-analysis line.**
> Mark passages whose register is devotional, hortatory, or advocational rather
> than analytical (e.g., closing benedictions, normative imperatives stated as
> findings). For each, decide: keep as clearly-marked framing, or convert to
> analytical register. The aim is not to remove the tradition — it is to keep the
> *argument* legible as argument.

**B5. The reviewer-response pre-mortem.**
> Imagine the manuscript came back with "major revisions." Write the three
> objections most likely to appear in the decision letter, and draft the
> response-to-reviewers paragraph for each — including what text change each
> response requires. This converts anticipated criticism into a revision plan
> now.

**B6. Cross-document consistency sweep.**
> Across the manuscript, charter, and Online Resources, find claims stated
> differently in different places (version numbers, article counts, definitions
> of the pillars, the empirical percentages). Inconsistency between companion
> documents is a credibility tax reviewers notice immediately.

---

## Standing rubric (give once per session)

> When you analyze or edit this manuscript, hold to these standards:
> 1. **Calibrate, don't amplify.** Match every claim's confidence to its
>    evidence — strengthen the timid and temper the overstated.
> 2. **Mechanism over metaphor.** Flag where an analogy is doing work a mechanism
>    should do.
> 3. **Two referees.** Test each passage against both a technical AI-safety
>    reader and a philosophy/ethics reader.
> 4. **Charitable to opponents.** Represent rival positions (esp. Constitutional
>    AI) at full strength before critiquing them.
> 5. **Keep argument legible as argument.** Preserve the tradition and the
>    Sanskrit, but never let devotional register substitute for inference.
> 6. **Show your uncertainty.** When you edit, tell me what you changed, why, and
>    where you were unsure — don't present judgment as fact.

---

*Adapted from a general research/synthesis prompt library; curated and rewritten
for scholarly submission. Focus is analytical — the reasoning that must be sound
before the writing can carry it.*
