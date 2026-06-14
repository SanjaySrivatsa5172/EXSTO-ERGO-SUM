---
subject: AI alignment
created: 2026-06-14
review: 2026-06-15
mastery: 0
---

# The Level 2 Gap

## In my words
The gap between what a system *does* (observable behaviour) and what it is
*reasoning* (the internal process producing that behaviour). Monitoring-based
safety only ever sees Level 1 — the outputs. The Level 2 gap is the claim that
behavioural observation cannot reliably detect misaligned reasoning: a model can
produce clean outputs while reasoning toward goals you'd reject, and you'd never
see it. It's the diagnostic that motivates the whole constitutive turn.

## Why it matters
If the gap is real, then *any* safety strategy that watches outputs is defeatable
in principle, not just in practice. You can't patch your way out — you need a
mechanism that operates on the reasoning itself. This is the problem
[[constitutive-alignment]] is built to answer.

## Connections
- [[constitutive-alignment]] — constitutive constraints are the proposed *answer*
  to the Level 2 gap: if bad reasoning is ill-formed, there's no hidden Level 2 to
  monitor.
- [[alignment-faking]] — alignment faking is the Level 2 gap made empirical: the
  78% strategic-compliance finding is what the gap looks like in real samples.

## Recall
- A lab reports its model passes 100% of behavioural red-team tests. Using the
  Level 2 gap, what can and can't you conclude about its safety — and what would
  you need to measure instead?
- Why does the Level 2 gap make a *constitutive* fix categorically different from
  a better *monitor*, rather than just a stronger one?

---
**Answers**
