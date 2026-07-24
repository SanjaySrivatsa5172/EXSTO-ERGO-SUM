export const meta = {
  name: 'seo-content-machine',
  description: 'SEO content graph: three parallel research scouts (top-page coverage, real user questions, content gaps) merge into an outline and full draft, a fact-checker flags every claim without a source, and the draft lands in drafts/ with the flags on top. Draft-only — nothing is ever published.',
  whenToUse: 'Run via /seo-draft <topic> when the author wants one ranking-ready website content draft. Output is a file in drafts/ awaiting webmaster review; publishing is a human decision this graph cannot make.',
  phases: [
    { title: 'Research', detail: 'three parallel scouts: top-page coverage, real questions, content gaps' },
    { title: 'Draft', detail: 'one merge node folds the research into an outline, then writes the full draft' },
    { title: 'Verify', detail: 'fact-checker flags every claim without a source' },
    { title: 'Save', detail: 'write drafts/<date>-<slug>.md with the flagged claims at the top' },
  ],
}

// ── Args: topic required; audience/notes optional ──────────────────────────
const topic =
  typeof args === 'string' ? args.trim()
  : (args && typeof args.topic === 'string') ? args.topic.trim()
  : ''
if (!topic) {
  throw new Error('No topic given. Invoke as /seo-draft <topic>, or Workflow({name: "seo-content-machine", args: {topic: "…"}}).')
}
const audience = (args && typeof args === 'object' && args.audience) ? String(args.audience) : ''
const notes = (args && typeof args === 'object' && args.notes) ? String(args.notes) : ''
const brief = [
  `Topic: ${topic}`,
  audience && `Target audience: ${audience}`,
  notes && `Site/context notes: ${notes}`,
].filter(Boolean).join('\n')

// ── Contracts: every node returns a bounded, validated shape ───────────────
// Every research scout must declare how much of the live web it actually
// reached, so downstream nodes (and the saved draft) can label provenance
// honestly instead of passing model memory off as research.
const WEB_ACCESS = { type: 'string', enum: ['full', 'partial', 'blocked'] }

const COVERAGE = {
  type: 'object', additionalProperties: false,
  properties: {
    webAccess: WEB_ACCESS,
    pages: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          url: { type: 'string' },
          title: { type: 'string' },
          covers: { type: 'array', items: { type: 'string' } },
          format: { type: 'string' },
          angle: { type: 'string' },
        },
        required: ['url', 'title', 'covers'],
      },
    },
    commonThemes: { type: 'array', items: { type: 'string' } },
    titlePatterns: { type: 'array', items: { type: 'string' } },
    typicalDepth: { type: 'string' },
  },
  required: ['webAccess', 'pages', 'commonThemes'],
}

const QUESTIONS = {
  type: 'object', additionalProperties: false,
  properties: {
    webAccess: WEB_ACCESS,
    questions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          question: { type: 'string' },
          whereSeen: { type: 'string' },
          intent: { type: 'string' },
        },
        required: ['question', 'whereSeen'],
      },
    },
    themes: { type: 'array', items: { type: 'string' } },
  },
  required: ['webAccess', 'questions'],
}

const GAPS = {
  type: 'object', additionalProperties: false,
  properties: {
    webAccess: WEB_ACCESS,
    gaps: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          gap: { type: 'string' },
          evidence: { type: 'string' },
          opportunity: { type: 'string' },
        },
        required: ['gap', 'evidence'],
      },
    },
    weaknesses: { type: 'array', items: { type: 'string' } },
  },
  required: ['webAccess', 'gaps'],
}

const DRAFT = {
  type: 'object', additionalProperties: false,
  properties: {
    title: { type: 'string' },
    slug: { type: 'string' },
    metaDescription: { type: 'string' },
    targetKeywords: { type: 'array', items: { type: 'string' } },
    outline: { type: 'array', items: { type: 'string' } },
    body: { type: 'string' },
  },
  required: ['title', 'slug', 'outline', 'body'],
}

const FACTCHECK = {
  type: 'object', additionalProperties: false,
  properties: {
    totalClaims: { type: 'number' },
    flagged: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          section: { type: 'string' },
          problem: { type: 'string' },
          suggestedSource: { type: 'string' },
        },
        required: ['claim', 'section', 'problem'],
      },
    },
  },
  required: ['totalClaims', 'flagged'],
}

const SAVED = {
  type: 'object', additionalProperties: false,
  properties: {
    path: { type: 'string' },
    bytes: { type: 'number' },
  },
  required: ['path'],
}

// Shared preamble so every node honors this repo's honesty discipline.
const GROUND_RULES = `You are a node in the seo-content-machine graph, producing
website content for this repository's author. Honesty rules, non-negotiable:
- Research means retrieved evidence. Use WebSearch first; WebFetch is
  best-effort (this environment's network policy may block general egress with
  403 — that is a policy denial, do not retry or route around it).
- Never fabricate a page, question, statistic, quote, or URL. If you could not
  retrieve real data, say so in your output instead of inventing it.
- Report webAccess honestly: 'full' if you opened real pages, 'partial' if you
  only saw search results/snippets, 'blocked' if nothing external was reachable.
- Repo discipline: do not edit, create, or delete any repository file unless
  your node's instructions explicitly name the file to write. Never run
  git commit or git push. Never post, upload, or publish anything anywhere —
  publishing is a human (webmaster) decision outside this graph.`

// ── Phase 1 — Research: three scouts at once, blind to each other ──────────
// Barrier justified: the merge node genuinely needs all three payloads.
phase('Research')
log(`Researching "${topic}" — three scouts in parallel`)

const [coverage, questions, gaps] = await parallel([
  () => agent(`${GROUND_RULES}

${brief}

Node: SERP coverage. Find what the CURRENT top-ranking pages for this topic
cover. WebSearch the topic (plus one or two close phrasings); open the
strongest 5–8 results with WebFetch where egress allows. For each page report
url, title, what it covers (section-level list), format (guide, listicle,
docs, comparison…), and its angle. Then the cross-page picture: commonThemes
every top page hits, titlePatterns, typicalDepth (rough word count and
thoroughness). Only report pages you actually saw in results — never invent
a URL.`,
    { label: 'research:coverage', phase: 'Research', schema: COVERAGE }),

  () => agent(`${GROUND_RULES}

${brief}

Node: real questions. Find the questions REAL people ask about this topic —
not questions you imagine they might ask. Mine search results for
People-Also-Ask style questions, and search forums (site:reddit.com, Stack
Exchange, Quora, niche communities) for how people actually phrase their
problems. Report each question with whereSeen (the surface you found it on)
and intent (informational, comparison, troubleshooting, purchase…). Group
recurring themes. A question you could not ground in a real surface does not
belong in the list.`,
    { label: 'research:questions', phase: 'Research', schema: QUESTIONS }),

  () => agent(`${GROUND_RULES}

${brief}

Node: content gaps. Find what the top-ranking pages SKIP. Independently search
the topic and open several top results, then hunt for: subtopics people raise
in forums or comments that the ranking pages never address, questions the
pages pose but never answer, missing formats (no worked example, no data, no
comparison table), and outdated or thin sections. For each gap give evidence
(which pages skip it, how you know readers want it) and the opportunity it
represents. Gaps must come from observed absence, not imagination.`,
    { label: 'research:gaps', phase: 'Research', schema: GAPS }),
])

// Edge work in plain JS: tolerate a dead scout, but never draft from nothing.
const legs = [
  ['top-page coverage', coverage],
  ['real user questions', questions],
  ['content gaps', gaps],
]
const dead = legs.filter(([, r]) => !r).map(([name]) => name)
if (dead.length === legs.length) {
  throw new Error('All three research scouts failed — refusing to draft from model memory alone.')
}
if (dead.length > 0) {
  log(`⚠ Coverage gap: no result for ${dead.join(', ')} — drafting on partial research`)
}
const aliveLegs = legs.filter(([, r]) => r)
if (aliveLegs.every(([, r]) => r.webAccess === 'blocked')) {
  throw new Error('Network egress was blocked for every research scout — a draft would be fabricated from model memory. Run /seo-draft from a session with open-web access (e.g. the desktop app) instead.')
}
const provenance = aliveLegs.map(([name, r]) => `${name}: ${r.webAccess}`).join(' · ')
log(`Research provenance — ${provenance}`)

// ── Phase 2 — Draft: one merge node writes outline, then the full draft ────
phase('Draft')
const draft = await agent(`${GROUND_RULES}

${brief}

Node: the merge. Below are the three research payloads (JSON). First fold them
into ONE outline: coverage parity with what every top page hits, the real
questions answered as sections or an FAQ, and the gaps as the sections that
make this the more complete page. Then write the FULL draft in markdown — a
ranking-ready page, not an abstract: a direct answer near the top of each
section, concrete specifics, scannable headings, no filler. Where a fact came
from the research, keep its source URL inline as a markdown link. Where a fact
comes from general knowledge, leave it plain — the fact-checker downstream
flags what lacks a source. Never invent a source to dress up a claim.

Coverage payload: ${coverage ? JSON.stringify(coverage) : '(scout failed — unavailable)'}
Questions payload: ${questions ? JSON.stringify(questions) : '(scout failed — unavailable)'}
Gaps payload: ${gaps ? JSON.stringify(gaps) : '(scout failed — unavailable)'}`,
  { label: 'draft:merge+write', phase: 'Draft', schema: DRAFT, effort: 'high' })
if (!draft) throw new Error('The draft node failed — nothing to verify or save.')
log(`Draft written: "${draft.title}" (${draft.outline.length} outline sections)`)

// ── Phase 3 — Verify: the fact-checker gate ────────────────────────────────
phase('Verify')
const check = await agent(`${GROUND_RULES}

Node: fact-checker gate. Below is a draft destined for the author's website.
Extract EVERY factual claim — statistics, dates, named findings, tool or
product behavior, "studies show", comparisons, prices, anything falsifiable —
and count them (totalClaims). Then flag every claim without a source: no
inline link, or a link that does not actually support the sentence
(spot-check the load-bearing ones with WebFetch/WebSearch where egress
allows). For each flagged claim report it verbatim, the section it sits in,
the problem (uncited / source does not support it / could not verify), and a
suggestedSource ONLY if you actually found a real one — otherwise omit the
field. An honest flag beats a decorated guess.

DRAFT TITLE: ${draft.title}
DRAFT BODY:
${draft.body}`,
  { label: 'verify:fact-check', phase: 'Verify', schema: FACTCHECK, effort: 'high' })
if (!check) {
  log('⚠ Fact-checker failed — the draft will be saved marked UNCHECKED; treat every claim as unverified')
} else {
  log(`Fact-check: ${check.flagged.length} of ${check.totalClaims} claims flagged`)
}

// ── Phase 4 — Save: the graph's only writer, one new file in drafts/ ───────
phase('Save')
const flagsBlock = check
  ? (check.flagged.length
      ? check.flagged.map((f, i) =>
          `${i + 1}. "${f.claim}" — ${f.section} — ${f.problem}${f.suggestedSource ? ` — candidate source: ${f.suggestedSource}` : ''}`,
        ).join('\n')
      : '(none — the fact-checker found a source behind every claim)')
  : '(FACT-CHECK FAILED TO RUN — treat every claim in this draft as unverified)'

const saved = await agent(`${GROUND_RULES}

Node: save. This node is the graph's ONLY writer, and it writes exactly one
NEW file inside the repository's drafts/ directory — nothing else. Create the
directory if it is missing. Do not commit, do not push, do not touch any
existing file.

1. Get today's date in ISO form: date +%F
2. Path: drafts/<date>-<slug>.md using slug "${draft.slug}" (kebab-case it if
   it is not already). If the path exists, append -2, -3, … — never overwrite.
3. Write the file EXACTLY in this shape (angle brackets are placeholders to
   fill; keep everything else verbatim, including the NOT PUBLISHED banner):

---
topic: ${JSON.stringify(topic)}
title: ${JSON.stringify(draft.title)}
meta_description: <the meta description given below, or omit this line if none>
target_keywords: <the keywords given below comma-joined, or omit this line if none>
research_provenance: <the provenance line given below>
generated: <date>
workflow: seo-content-machine
status: DRAFT — NOT PUBLISHED. Do not publish without webmaster review.
---

## ⚠ Fact-check flags — resolve before publishing

<the flags block given below, verbatim>

---

<the draft body given below, verbatim; prepend an H1 of the title only if the
body does not already start with one>

4. Return {path, bytes} for the file you wrote.

meta description: ${draft.metaDescription || '(none)'}
target keywords: ${(draft.targetKeywords || []).join(', ') || '(none)'}
provenance line: ${provenance}
flags block:
${flagsBlock}

draft body:
${draft.body}`,
  { label: 'save:drafts', phase: 'Save', schema: SAVED, effort: 'low' })

// ── Result ─────────────────────────────────────────────────────────────────
const result = {
  topic,
  state: !check ? 'draft-unchecked' : (check.flagged.length ? 'draft-flagged' : 'draft-clean'),
  draftPath: saved ? saved.path : null,
  title: draft.title,
  outline: draft.outline,
  researchProvenance: provenance,
  factCheck: check
    ? { totalClaims: check.totalClaims, flagged: check.flagged }
    : 'FAILED — treat every claim as unverified',
  humanGate: 'Nothing was published and nothing was committed. The draft waits in drafts/ for webmaster review; publishing is a human decision outside this graph.',
}
if (!saved) {
  result.error = 'save node failed — draft returned inline so nothing is lost'
  result.unsavedDraft = {
    metaDescription: draft.metaDescription,
    targetKeywords: draft.targetKeywords,
    flagsBlock,
    body: draft.body,
  }
}
return result
