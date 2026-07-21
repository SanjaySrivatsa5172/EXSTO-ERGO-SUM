export const meta = {
  name: 'pm-status',
  description: 'Project-manager graph: parallel scouts sweep the submission project, a skeptic panel verifies high-severity findings, one top-tier node synthesizes a status report with ranked next actions',
  whenToUse: 'Run for a full project pulse — repo state, version/count drift, verification debt, submission readiness, tooling health. The /pm command invokes this by name.',
  phases: [
    { title: 'Scout', detail: 'five parallel scouts, one bounded area each' },
    { title: 'Verify', detail: 'skeptic panel on high-severity findings only' },
    { title: 'Synthesize', detail: 'one PM report with ranked next actions' },
  ],
}

// ── Contracts (course step 03: every node gets a bounded, validated shape) ──
const FINDINGS = {
  type: 'object', additionalProperties: false,
  properties: {
    summary: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          area: { type: 'string' },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          claim: { type: 'string' },
          evidence: { type: 'string' },
          suggestedAction: { type: 'string' },
        },
        required: ['area', 'severity', 'claim', 'evidence', 'suggestedAction'],
      },
    },
  },
  required: ['summary', 'findings'],
}

const VERDICT = {
  type: 'object', additionalProperties: false,
  properties: {
    refuted: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['refuted', 'reason'],
}

// Shared preamble so every scout honors this repo's discipline.
const GROUND_RULES = `You are a scout node in a project-status graph for the
EXSTO ERGO SUM repository — an academic submission (manuscript + charter +
online resources, journal: AI and Ethics), not a software project. Read-only:
never edit, create, or delete repository files. The .tex sources are NOT
committed; the PDFs are the in-repo deliverables and derived/*.txt are their
readable mirrors. Cite evidence as file:line where possible. Preserve Sanskrit
diacritics exactly (Ahiṃsā, Saṃskāra-Vyākaraṇa, Sat-Cit-Ānanda, Pañca-Stambha).
Report findings, not fixes. Severity: high = could block or embarrass a journal
submission; medium = should be fixed before submission; low = polish.`

const focus = (args && args.focus) ? `\nThe author asked you to weight this focus area: ${args.focus}` : ''

// ── Phase 1 — Scout (course step 05: fan out; step 12: cheap tier for bounded jobs) ──
phase('Scout')

const SCOUTS = [
  {
    key: 'repo',
    prompt: `${GROUND_RULES}${focus}
Area: repository state. Report: current branch and cleanliness (git status),
last 5 commits (git log --oneline), whether all seven deliverable PDFs exist
(manuscript, manuscript_condensed, charter, onlineresources, coverletter,
titlepage, titlepage_with_author) with a derived/*.txt mirror for each, and
whether open-loop files exist (HANDOFF.md, SOURCES.md) and what they leave
unfinished. Flag anything stale, missing, or uncommitted as a finding.`,
  },
  {
    key: 'versions',
    prompt: `${GROUND_RULES}${focus}
Area: version and count agreement (quick signal, not the deep sweep). Grep
README.md and derived/*.txt for the Charter version string (a "v3.xx" form),
the article count, the Part count, and the pillar count. Do NOT assume a
canonical value — report every occurrence and flag disagreements between files
as findings (high severity if README disagrees with the manuscript set).`,
  },
  {
    key: 'verification',
    prompt: `${GROUND_RULES}${focus}
Area: verification debt. Read VERIFICATION.md (and SOURCES.md if present).
Report: how many claims are recorded as verified / mismatched / unsupported /
unverifiable, which document sections or OR clusters have not been swept at
all, and any verdict recorded as blocked by network egress that still awaits a
primary-source read. Each unswept area or unresolved verdict is a finding.`,
  },
  {
    key: 'submission',
    prompt: `${GROUND_RULES}${focus}
Area: submission readiness. Check README.md's citation block and stated
submission status against derived/coverletter.txt and both title pages
(derived/titlepage.txt anonymized, derived/titlepage_with_author.txt with
identity). Report: journal name consistency, author/ORCID/affiliation
consistency, license statements (CC BY-NC-SA 4.0) not contradicting each
other, and whether the anonymized title page actually anonymizes. Flag
mismatches as findings.`,
  },
  {
    key: 'tooling',
    prompt: `${GROUND_RULES}${focus}
Area: Claude tooling health. Verify .claude/ is coherent: settings.json hooks
point at scripts that exist and are executable, commands/*.md and agents/*.md
frontmatter is well-formed, rules/*.md exist, workflows/*.js begin with an
'export const meta' block, and CLAUDE.md's tooling section matches what is
actually on disk (no documented-but-missing or present-but-undocumented
pieces). Flag drift as findings.`,
  },
]

const scoutResults = await parallel(
  SCOUTS.map((s) => () =>
    agent(s.prompt, {
      label: `scout:${s.key}`,
      phase: 'Scout',
      schema: FINDINGS,
      effort: 'low', // course step 12: bounded, repetitive nodes ride the cheap tier
    })),
)

// ── Edge work in plain JS (course step 04: flatten/dedupe is code, zero tokens) ──
// Course step 10: tolerate missing inputs — a dead scout must not sink the run.
// Attach scout names BEFORE filtering nulls, or a dead scout shifts the
// indices and every later finding gets misattributed.
const alive = scoutResults
  .map((r, i) => (r ? { scout: SCOUTS[i].key, ...r } : null))
  .filter(Boolean)
const dropped = SCOUTS.length - alive.length
if (dropped > 0) log(`Coverage gap: ${dropped} of ${SCOUTS.length} scouts returned nothing — reporting on partial evidence`)

const seen = new Set()
const findings = alive
  .flatMap((r) => r.findings.map((f) => ({ ...f, scout: r.scout })))
  .filter((f) => {
    const key = `${f.area}::${f.claim}`.toLowerCase()
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })

const high = findings.filter((f) => f.severity === 'high')
const watchlist = findings.filter((f) => f.severity !== 'high')
log(`Scouts back: ${findings.length} findings (${high.length} high, ${watchlist.length} watchlist)`)

// ── Phase 2 — Verify (course step 08: route in code; step 09: skeptics gate the edge) ──
let confirmedHigh = []
let rejectedHigh = []
if (high.length === 0) {
  log('Router: no high-severity findings — skipping the verify phase entirely')
} else {
  phase('Verify')
  const LENSES = [
    'reproduce: re-read the cited evidence yourself — does the file actually say what the finding claims, at that location?',
    'severity: accept the fact but attack the rating — would this genuinely block or embarrass a journal submission, or is it watchlist noise?',
    'staleness: hunt for evidence the issue is already resolved elsewhere in the repo (a later commit, VERIFICATION.md, a corrected file) making this finding out of date.',
  ]
  const judged = await parallel(high.map((f) => () =>
    parallel(LENSES.map((lens) => () =>
      agent(
        `${GROUND_RULES}
You are a skeptic on a verifier gate. One lens only —
${lens}
The finding under attack (from scout "${f.scout}"):
${JSON.stringify(f, null, 2)}
Try to refute it. If you cannot check the evidence, default to refuted=true.`,
        { label: `skeptic:${lens.split(':')[0]}`, phase: 'Verify', schema: VERDICT },
      )))
      .then((votes) => {
        const cast = votes.filter(Boolean)
        const surviving = cast.filter((v) => !v.refuted).length
        return { finding: f, survives: surviving >= 2, votes: cast }
      })))
  const settled = judged.filter(Boolean)
  confirmedHigh = settled.filter((j) => j.survives).map((j) => j.finding)
  rejectedHigh = settled
    .filter((j) => !j.survives)
    .map((j) => ({ ...j.finding, refutations: j.votes.filter((v) => v.refuted).map((v) => v.reason) }))
  log(`Verifier gate: ${confirmedHigh.length} of ${high.length} high findings survived the panel`)
}

// ── Phase 3 — Synthesize (course step 07: the merge node; step 12: judgment gets the effort) ──
phase('Synthesize')
const report = await agent(
  `${GROUND_RULES}
You are the project-manager node — the single merge point of a status graph.
Write the PM status report for the author (a physician-scholar preparing this
journal submission), in scholarly but plain prose, as markdown. Do not invent
facts beyond the inputs. Do not stamp a date. Structure:

# EXSTO ERGO SUM — project status
One-line overall state (on track / needs attention / blocked), then:
## State of the project   — 3–6 sentences from the scout summaries
## Confirmed risks        — the panel-verified high findings, with evidence
## Watchlist              — medium/low findings, one line each (unverified)
## Discarded by the panel — refuted "high" findings and why (transparency)
## Next actions           — numbered, ranked hardest-consequence-first; each a
                            single imperative sentence naming its file(s)

Inputs:
Scout summaries: ${JSON.stringify(alive.map((r) => ({ scout: r.scout, summary: r.summary })))}
Confirmed high findings: ${JSON.stringify(confirmedHigh)}
Refuted high findings: ${JSON.stringify(rejectedHigh)}
Watchlist: ${JSON.stringify(watchlist)}

Return ONLY the markdown report.`,
  { label: 'pm:synthesize', phase: 'Synthesize', effort: 'high' },
)

return {
  state: confirmedHigh.length > 0 ? 'needs-attention' : 'on-track',
  confirmedHigh,
  watchlist,
  rejectedHigh,
  report,
}
