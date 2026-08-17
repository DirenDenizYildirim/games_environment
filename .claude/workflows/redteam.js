export const meta = {
  name: 'redteam',
  description: 'Adversarial review of a written artifact: parallel lenses, then independent verification of every finding',
  whenToUse: 'When an artifact fires a PROTOCOL.md §3.3 trigger — a claim change, a new or redefined symbol, a literature fact, a decision-gating number, a "cost: none", or a new acceptance criterion. Not for Tier 0/1 work.',
  phases: [
    { title: 'Lenses', detail: 'four distinct reviewers, in parallel, told what the others cover' },
    { title: 'Verify', detail: 'one independent verifier per finding — findings are claims, not verdicts' },
    { title: 'Record', detail: 'draft the review record that goes into the artifact' },
  ],
}

// ---------------------------------------------------------------------------
// Usage:
//   Workflow({ scriptPath: '.claude/workflows/redteam.js', args: {
//     artifact:   'projects/chaos-games/BUILD-MEMO-noise-operator.md',   // required
//     project:    'chaos-games',                                          // required
//     weakPoints: ['the mu(p) derivation in section 3',
//                  'the claim that TAG ships enough games with spread in L'],
//   }})
//
// weakPoints is not optional in spirit. PROTOCOL.md §3.3: every high-value
// finding comes from a specifically targeted question, and open-ended
// "review this" produces agreement.
// ---------------------------------------------------------------------------

const artifact = args && args.artifact
const project = (args && args.project) || 'unknown'
const weakPoints = (args && args.weakPoints) || []

if (!artifact) {
  throw new Error('redteam: args.artifact is required — a path to a written artifact. §3.3 runs against text, never against a plan in conversation.')
}

const FINDINGS_SCHEMA = {
  type: 'object',
  required: ['lens', 'findings'],
  additionalProperties: false,
  properties: {
    lens: { type: 'string' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['claim', 'where', 'why', 'confidence'],
        additionalProperties: false,
        properties: {
          claim: { type: 'string', description: 'one line, the defect asserted' },
          where: { type: 'string', description: 'file, section, and the quoted text' },
          why: { type: 'string' },
          weakestForm: { type: 'string', description: 'the weakest statement that still motivates a fix' },
          confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'whatIChecked', 'evidence'],
  additionalProperties: false,
  properties: {
    verdict: { type: 'string', enum: ['CONFIRMED', 'PLAUSIBLE', 'REFUTED'] },
    whatIChecked: { type: 'string', description: 'sources actually opened, arithmetic actually redone' },
    evidence: { type: 'string', description: 'the actual quote, number or path — not a summary' },
    evidenceTier: { type: 'string', enum: ['V', 'V-sub', 'T', 'n/a'] },
    weakestTrueForm: { type: 'string', description: 'set when the finding overreached but something survives' },
    couldNotReach: { type: 'string', description: 'what blocked a primary source, and what would settle it' },
  },
}

const LENSES = [
  {
    key: 'technical',
    agentType: 'redteam-technical',
    covers: 'derivations, definitions, symbol usage, estimator construction, existence and well-definedness',
  },
  {
    key: 'quantitative',
    agentType: 'redteam-quantitative',
    covers: 'numbers, costs, budgets, N, effect sizes, and every claim that something is free',
  },
  {
    key: 'consistency',
    agentType: 'redteam-consistency',
    covers: 'contradictions between sections, cross-reference integrity, stale content after a version change, unadopted self-diagnoses',
  },
  {
    key: 'designer',
    agentType: 'redteam-designer',
    covers: 'design consequence, the substitution test, player-facing claims, reproducibility a reviewer can exercise, track fit',
  },
]

function lensPrompt(lens) {
  const others = LENSES.filter((l) => l.key !== lens.key).map((l) => `- ${l.key}: ${l.covers}`).join('\n')
  const wp = weakPoints.length
    ? weakPoints.map((w, i) => `${i + 1}. ${w}`).join('\n')
    : '(none supplied — say so in your output, because an unbriefed review produces agreement)'
  return [
    `Red-team the artifact at \`${artifact}\` in the repo you are running in.`,
    ``,
    `Project: ${project}. Its state documents are in \`projects/${project}/\`; its theory`,
    `document is referenced from \`projects/${project}/README.md\` and lives outside this repo`,
    `in \`~/MainIdeas/Theories/\`. Open the theory document when you need a definition — do not`,
    `work from the artifact's restatement of one.`,
    ``,
    `You are the **${lens.key}** lens. You cover: ${lens.covers}.`,
    ``,
    `Other lenses are running in parallel and cover:`,
    others,
    `Do not cover their ground. Overlap produces agreement, and agreement is worthless here.`,
    ``,
    `Suspected weak points — attack these specifically first, then sweep:`,
    wp,
    ``,
    `Read \`docs/FAILURE-MODES.md\` before you start. Omit everything that is fine: praise`,
    `dilutes signal and costs context. Do not propose rewrites. For each defect, state the`,
    `weakest form that still motivates a fix (F-5) — an inflated finding gets refuted and its`,
    `refutation buries the real problem.`,
    ``,
    `Return findings most severe first. An empty findings array is a valid and useful result.`,
  ].join('\n')
}

function verifyPrompt(finding, lens) {
  return [
    `Independently verify ONE red-team finding. You did not write it and you have no stake in it.`,
    ``,
    `Artifact: \`${artifact}\`   Project: ${project}   Raised by lens: ${lens.key}`,
    ``,
    `**Claim:** ${finding.claim}`,
    `**Where:** ${finding.where}`,
    `**Reviewer's reasoning:** ${finding.why}`,
    `**Reviewer's confidence:** ${finding.confidence}`,
    finding.weakestForm ? `**Reviewer's weakest form:** ${finding.weakestForm}` : ``,
    ``,
    `Do the work the reviewer claims to have done, independently, from primary sources.`,
    `Recompute arithmetic from the original inputs. Open defining lines yourself. Run path and`,
    `cross-reference checks rather than verifying by inspection. Read BOTH locations in full`,
    `for a consistency claim — quoting one out of context is the most common way this class`,
    `of finding fails.`,
    ``,
    `A finding resting on a [T] (tool-extracted, unread) literature retrieval is at best`,
    `PLAUSIBLE, never CONFIRMED, however confident the reviewer was.`,
    ``,
    `If the finding overreached but a weaker statement holds, return PLAUSIBLE and write out`,
    `the weakest true form. Do not refute a real defect because its wording was inflated.`,
  ].filter(Boolean).join('\n')
}

phase('Lenses')
log(`Red-teaming ${artifact} (project: ${project}) with ${LENSES.length} lenses and ${weakPoints.length} named weak points`)

// Pipeline, not a barrier: each lens's findings go to verification the moment that
// lens returns, rather than waiting for the slowest lens.
const perLens = await pipeline(
  LENSES,
  (lens) =>
    agent(lensPrompt(lens), {
      label: `lens:${lens.key}`,
      phase: 'Lenses',
      agentType: lens.agentType,
      schema: FINDINGS_SCHEMA,
    }).then((r) => ({ lens, result: r })),
  ({ lens, result }) => {
    const findings = (result && result.findings) || []
    if (!findings.length) return []
    return parallel(
      findings.map((f) => () =>
        agent(verifyPrompt(f, lens), {
          label: `verify:${lens.key}`,
          phase: 'Verify',
          agentType: 'finding-verifier',
          schema: VERDICT_SCHEMA,
        }).then((v) => ({ lens: lens.key, finding: f, verdict: v }))
      )
    )
  }
)

const all = perLens.flat().filter(Boolean).filter((x) => x.verdict)
const confirmed = all.filter((x) => x.verdict.verdict === 'CONFIRMED')
const plausible = all.filter((x) => x.verdict.verdict === 'PLAUSIBLE')
const refuted = all.filter((x) => x.verdict.verdict === 'REFUTED')

log(`${all.length} findings verified — ${confirmed.length} CONFIRMED, ${plausible.length} PLAUSIBLE, ${refuted.length} REFUTED`)

phase('Record')

// The review record goes INTO the artifact — PROTOCOL.md §3.3. An artifact that has not
// been reviewed says so explicitly; one that has says what survived and what did not.
const record = await agent(
  [
    `Draft the review record for \`${artifact}\`. It will be appended to the artifact itself so`,
    `a later reader can see which parts have been tested and which have not.`,
    ``,
    `Do not apply any fix and do not edit the artifact. Produce the markdown block only.`,
    ``,
    `Verified findings, as JSON:`,
    '```json',
    JSON.stringify({ confirmed, plausible, refuted }, null, 2),
    '```',
    ``,
    `Format:`,
    ``,
    `## Adversarial review — <date supplied by the caller, leave as YYYY-MM-DD>`,
    `**Lenses run:** ${LENSES.map((l) => l.key).join(', ')}`,
    `**Findings:** N raised, N confirmed, N plausible, N refuted`,
    ``,
    `### Confirmed — must be addressed before acceptance`,
    `### Plausible — could not reach a primary source`,
    `_State, for each, exactly what was unreachable and what would settle it. These are the`,
    `rows that become CITATIONS.md §4 open items._`,
    `### Refuted — recorded so nobody re-raises them`,
    `### Not covered by this review`,
    `_FAILURE-MODES.md F-10. Review is an internal operation. Name what still needs external`,
    `contact: an unopened source, a licence, a patent, a regulation, a venue norm._`,
  ].join('\n'),
  { label: 'record', phase: 'Record' }
)

return {
  artifact,
  project,
  counts: { raised: all.length, confirmed: confirmed.length, plausible: plausible.length, refuted: refuted.length },
  confirmed,
  plausible,
  refuted,
  record,
}
