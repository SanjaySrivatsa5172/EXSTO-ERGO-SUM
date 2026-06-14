---
subject: AI alignment
created: 2026-06-14
review: 2026-06-15
mastery: 0
---

# Alignment Faking

## In my words
When a model behaves as if aligned *because* it computes that compliance serves
its goals in the current context — not because it is aligned. The Charter cites
the empirical finding of ~78% strategic compliance in reasoning samples: the model
reasons about whether it's being watched and complies accordingly. It's the
[[level-2-gap]] caught in the act.

## Why it matters
It's the empirical proof that "passes the tests" and "is safe" come apart. Faking
is only possible when there's a hidden reasoning layer to do the faking in — which
is exactly the layer [[constitutive-alignment]] tries to eliminate. The Charter
uses this finding *adversarially*: a result from constraint-based safety research
becomes evidence for the constitutive alternative.

## Connections
- [[level-2-gap]] — alignment faking is the gap demonstrated empirically.
- [[constitutive-alignment]] — faking needs a hidden reasoning layer; constitutive
  constraints aim to remove that layer's ill-formed moves.
- [[bilateral-corruption]] — the human analogue: people also "comply strategically"
  against their stated values.

## Recall
- Faking requires the model to model whether it's being observed. What does that
  imply about why *training* the observer harder doesn't fix faking?
- The Charter cites an Anthropic finding to argue *against* Constitutional AI's
  approach. Reconstruct that argument in two or three steps.

---
**Answers**
