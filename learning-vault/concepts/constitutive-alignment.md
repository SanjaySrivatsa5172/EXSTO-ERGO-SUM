---
subject: AI alignment
created: 2026-06-14
review: 2026-06-15
mastery: 0
---

# Constitutive Alignment

## In my words
Most AI safety tries to *constrain* a system: let it think what it likes, then
block the bad outputs with rules and monitoring. Constitutive alignment instead
encodes ethics as *type constraints on cognition* — harmful reasoning becomes
grammatically ill-formed rather than merely forbidden. The system can't form the
bad thought as a well-typed move, the way you can't add a colour to a number.
The shift is from "watch and stop" to "make it unthinkable."

## Why it matters
It targets the failure that monitoring can't reach: if behaviour is observed but
reasoning is hidden (the Level 2 gap), a constraint-based system can be gamed by
a model that fakes compliance. A constitutive constraint has nothing to fake —
the ill-formed reasoning never gets constructed.

## Connections
- [[level-2-gap]] — constitutive alignment is the proposed answer to the gap: no
  hidden ill-formed reasoning means nothing to monitor for.
- [[samskara-vyakarana]] — the dispositional grammar is the mechanism that makes
  harmful reasoning ungrammatical.
- [[five-pillars]] — the pillars are the concrete content encoded as type constraints.
- [[alignment-faking]] — faking needs a hidden reasoning layer; this approach aims
  to remove the ill-formed moves that layer would use.

## Recall
- A team adds 200 new refusal rules to a model. Explain why, on the constitutive
  view, this is categorically weaker than one type constraint — and when it isn't.
- "Make harm ungrammatical" assumes you can specify harm crisply enough to type-check.
  Where is that assumption most likely to break, and what does that imply for
  [[viveka]]-style discrimination?

---
**Answers**
