---
topic: classification
type: concept
source: stub — verify against CEAP 2020 revision
created: 2026-06-14
review: 2026-06-15
mastery: 0
---

# CEAP Classification

## In my words
The standard descriptive scheme for chronic venous disorders, four axes:
- **C** — Clinical class (C0 none → C6 active ulcer; C2 varicose veins, C3 oedema,
  C4 skin changes, C5 healed ulcer).
- **E** — Etiology (primary / secondary / congenital).
- **A** — Anatomy (superficial / deep / perforator).
- **P** — Pathophysiology (reflux / obstruction / both).

It's a *shared vocabulary*, not a severity score — it standardizes how a limb is
described so studies and clinics mean the same thing.

## Why it matters
For research it's the backbone of cohort definition: "C4–C6 with superficial
reflux" is a CEAP statement. Mixing CEAP classes in an analysis without stratifying
is a common way studies become uninterpretable. The P axis directly encodes the
reflux-vs-obstruction question that runs through [[venous-reflux]] and
[[may-thurner-syndrome]].

## Strength & caveats
Consensus standard, periodically revised (note the 2020 update). Limits: the C
axis is ordinal but not linear in severity, and inter-rater reliability for skin
classes (C4) is imperfect — worth checking before using C-class as an outcome.

## Connections
- [[chronic-venous-insufficiency]] — *describes*: CEAP is the vocabulary for staging
  a CVI limb.
- [[venous-reflux]] — *encodes*: reflux is one value of the P (pathophysiology) axis.
- [[may-thurner-syndrome]] — *encodes*: obstruction is the other P-axis value, often
  underweighted.
- [[endovenous-ablation]] — *stratifies-trials-of*: CEAP class is how ablation cohorts
  are defined and compared.
- [[reflux-severity-evaluation]] — *clinical-axis-of*: C-class (plus VCSS) is the
  clinical severity layer among the four axes.

## Questions
- The C axis is ordinal but not linear in severity. What goes wrong if you use C-class
  as a continuous outcome in a regression, and what's the fix?
- Inter-rater reliability for C4 (skin changes) is imperfect. Design a way to quantify
  how much that measurement noise could mask or fake a treatment effect.

---
**Answers / notes**
