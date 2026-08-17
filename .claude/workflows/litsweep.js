export const meta = {
  name: 'litsweep',
  description: 'Run the declared pre-emption search: fan term slices out to independent sweepers, assemble k, and report the surfaces not reached',
  whenToUse: 'Before any novelty claim, and before writing a positioning or related-work section. Its output is a reported number, not a verdict.',
  phases: [
    { title: 'Sweep', detail: 'one independent sweeper per term slice' },
    { title: 'Assemble', detail: 'dedup retrievals, adjudicate counts, produce k' },
  ],
}

// ---------------------------------------------------------------------------
// Usage:
//   Workflow({ scriptPath: '.claude/workflows/litsweep.js', args: {
//     claim:     'the collapse threshold is predictable from game structure',  // required
//     project:   'chaos-games',                                                // required
//     groupA:    ['execution noise', 'skill expression'],   // optional override
//     groupB:    ['game', 'Monte Carlo tree search'],       // optional override
//     groupC:    ['skill/luck ratio'],                      // optional override
//     maxSlices: 12,                                        // default 12
//   }})
//
// docs/SEARCH-PROTOCOL.md is the authority. The full term lists live there; the
// defaults below are a SUBSET chosen to keep a single run affordable.
//
// THE STOPPING RULE IN THE PROTOCOL IS TERM-LIST EXHAUSTION. A bounded run does
// not satisfy it. Every slice this script drops is logged and returned in
// `slicesNotRun`, and those belong in the archive's surfaces-not-reached
// section. A bounded run that does not record its bound is not a completed run.
// ---------------------------------------------------------------------------

const claim = args && args.claim
const project = (args && args.project) || 'unknown'
if (!claim) {
  throw new Error('litsweep: args.claim is required — one sentence. A sweep against "the project" returns everything and settles nothing.')
}

const DEFAULT_A = [
  'execution noise',
  'action noise',
  'skill expression',
  'outcome variance',
  'divergence',
  'indirect control',
]
const DEFAULT_B = [
  'game',
  'video game',
  'Monte Carlo tree search',
  'level design',
  'dynamic difficulty adjustment',
]
const DEFAULT_C = [
  'skill/luck ratio',
  'game refinement theory',
  'games needed to distinguish players',
  'agent-free difficulty metric',
  'finite-size Lyapunov exponent',
]

const A = (args && args.groupA) || DEFAULT_A
const B = (args && args.groupB) || DEFAULT_B
const C = (args && args.groupC) || DEFAULT_C
const maxSlices = (args && args.maxSlices) || 12

// Full cross product, in a stable order. No Math.random — runs must be resumable.
const allSlices = []
for (const a of A) for (const b of B) allSlices.push({ kind: 'pair', a, b, label: `${a} × ${b}` })
for (const c of C) allSlices.push({ kind: 'flat', c, label: `flat: ${c}` })

// Interleave pairs and flats so a bounded run still covers both groups, rather
// than spending its whole budget on the head of the cross product.
const pairs = allSlices.filter((s) => s.kind === 'pair')
const flats = allSlices.filter((s) => s.kind === 'flat')
const ordered = []
let pi = 0
let fi = 0
while (pi < pairs.length || fi < flats.length) {
  if (pi < pairs.length) ordered.push(pairs[pi++])
  if (pi < pairs.length) ordered.push(pairs[pi++])
  if (fi < flats.length) ordered.push(flats[fi++])
}

const slices = ordered.slice(0, maxSlices)
const slicesNotRun = ordered.slice(maxSlices).map((s) => s.label)

const SLICE_SCHEMA = {
  type: 'object',
  required: ['slice', 'queries', 'retrievals', 'surfacesNotReached'],
  additionalProperties: false,
  properties: {
    slice: { type: 'string' },
    queries: {
      type: 'array',
      description: 'exact query strings issued, verbatim, with the index used',
      items: { type: 'string' },
    },
    retrievals: {
      type: 'array',
      items: {
        type: 'object',
        required: ['work', 'tier', 'countsTowardK', 'why'],
        additionalProperties: false,
        properties: {
          work: { type: 'string', description: 'authors, title, venue, year' },
          identifier: { type: 'string', description: 'arXiv id, DOI, or URL if known' },
          tier: { type: 'string', enum: ['V', 'V-sub', 'T'] },
          countsTowardK: { type: 'boolean' },
          why: { type: 'string', description: 'count decision, and any setting mismatch to report in the differs-in-Y clause' },
        },
      },
    },
    forwardCitations: { type: 'string', description: 'which retrievals were followed forward and what came back; say so explicitly if none were' },
    surfacesNotReached: { type: 'string', description: 'paywalls, 403s, indices unavailable, languages, years — "none" if genuinely none' },
  },
}

function slicePrompt(slice) {
  const term = slice.kind === 'pair'
    ? `the term pair **${slice.a}** × **${slice.b}** (group A × group B)`
    : `the flat term **${slice.c}** (group C)`
  return [
    `Run one slice of the declared pre-emption search in \`docs/SEARCH-PROTOCOL.md\`.`,
    `Read that file first — it is the authority, including the venue list, the tier`,
    `definitions, the adjudication rule and the overloaded-term caveats.`,
    ``,
    `**Claim under test:** ${claim}`,
    `**Project:** ${project}`,
    `**Your slice:** ${term}`,
    ``,
    `Exhaust the slice. Do not stop when you find a satisfying answer — the stopping rule is`,
    `term exhaustion, not saturation and not judgment.`,
    ``,
    `Record every query verbatim. Tier every retrieval honestly: [V] read in the original,`,
    `[V-sub] partly read, [T] tool-extracted and not read. Most of yours will be [T] and that`,
    `is fine — inflating a tier is the worst thing you can do in this role, because every`,
    `downstream consumer trusts the tier and nothing else.`,
    ``,
    `Follow forward citations for anything close. That sweep is mandatory.`,
    ``,
    `A work counts toward k if it asks the question in ANY setting. Setting mismatch is`,
    `recorded, not subtracted. Ties resolve against novelty.`,
    ``,
    `Do not conclude anything about novelty. You produce retrievals and count decisions.`,
  ].join('\n')
}

phase('Sweep')
log(`Claim: ${claim}`)
log(`${ordered.length} slices in the full cross-product; running ${slices.length}, dropping ${slicesNotRun.length}`)
if (slicesNotRun.length) {
  log(`DROPPED SLICES (belong in surfaces-not-reached): ${slicesNotRun.join(' | ')}`)
}

const swept = await parallel(
  slices.map((s) => () =>
    agent(slicePrompt(s), {
      label: `sweep:${s.label}`,
      phase: 'Sweep',
      agentType: 'lit-sweeper',
      schema: SLICE_SCHEMA,
    })
  )
)

const good = swept.filter(Boolean)
const failed = slices.length - good.length
if (failed > 0) log(`${failed} slice(s) returned nothing — treat as surfaces not reached, not as k = 0`)

// Dedup across slices needs every slice in hand, so this barrier is real.
const seen = new Map()
for (const r of good) {
  for (const ret of r.retrievals || []) {
    const key = (ret.identifier || ret.work || '').toLowerCase().trim()
    if (!key) continue
    const prior = seen.get(key)
    if (!prior) {
      seen.set(key, { ...ret, foundIn: [r.slice] })
    } else {
      prior.foundIn.push(r.slice)
      // Keep the strongest tier and the most inclusive count decision.
      const rank = { V: 3, 'V-sub': 2, T: 1 }
      if ((rank[ret.tier] || 0) > (rank[prior.tier] || 0)) prior.tier = ret.tier
      if (ret.countsTowardK) prior.countsTowardK = true
    }
  }
}

const retrievals = Array.from(seen.values())
const counting = retrievals.filter((r) => r.countsTowardK)
const k = counting.length
const tierOfK = counting.some((r) => r.tier === 'V')
  ? (counting.every((r) => r.tier === 'V') ? 'V' : 'mixed')
  : (counting.some((r) => r.tier === 'V-sub') ? 'V-sub/T' : 'T')

log(`k = ${k} (tier: ${tierOfK}) from ${retrievals.length} deduplicated retrievals`)

phase('Assemble')

const archive = await agent(
  [
    `Assemble the LITSEARCH archive for this run. Format: \`docs/SEARCH-PROTOCOL.md\` §6.`,
    `Write the markdown only — do not create the file; the caller places it at`,
    `\`projects/${project}/LITSEARCH-<YYYY-MM-DD>.md\` and supplies the date.`,
    ``,
    `**Claim under test:** ${claim}`,
    `**k = ${k}**, evidence tier of k: **${tierOfK}**`,
    ``,
    `Slice results, as JSON:`,
    '```json',
    JSON.stringify(good, null, 2),
    '```',
    ``,
    `Deduplicated retrievals:`,
    '```json',
    JSON.stringify(retrievals, null, 2),
    '```',
    ``,
    `Slices in the cross-product that were NOT run (${slicesNotRun.length}):`,
    slicesNotRun.length ? slicesNotRun.map((s) => `- ${s}`).join('\n') : '- none',
    ``,
    `Produce, in order: the header (claim, upper cutoff = the run date, protocol version),`,
    `the exact queries issued, the retrieval table with tiers and count decisions, the`,
    `forward-citation sweep, the result sentence in the form`,
    `"This question has been asked in k retrieved works; the nearest is X; our claim differs`,
    `in Y" — and finally the **surfaces-not-reached** section.`,
    ``,
    `The surfaces-not-reached section is REQUIRED and must include the ${slicesNotRun.length}`,
    `unrun slices above, every paywall and 403, and anything a sweeper reported as unreached.`,
    `A run without that section is not a completed run.`,
    ``,
    `If k = 0, state plainly that this is a legitimate and WEAK result — the absence of`,
    `evidence against novelty over a bounded surface, not evidence of novelty.`,
  ].join('\n'),
  { label: 'archive', phase: 'Assemble' }
)

return {
  claim,
  project,
  k,
  tierOfK,
  retrievals,
  slicesRun: slices.map((s) => s.label),
  slicesNotRun,
  archive,
}
