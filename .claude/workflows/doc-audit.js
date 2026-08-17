export const meta = {
  name: 'doc-audit',
  description: 'Drift audit of a theory document against the seed it grew from — the FAILURE-MODES.md F-9 detector, run as four independent probes',
  whenToUse: 'Before accepting a large addition to a theory document, when a document has grown a lot since it was last read, or when you suspect a choice was adopted rather than made. Produces findings and ledger rows, never edits.',
  phases: [
    { title: 'Probe', detail: 'four independent probes: seed, vocabulary, self-diagnosis, choices' },
    { title: 'Report', detail: 'assemble the drift report and the ledger rows it implies' },
  ],
}

// ---------------------------------------------------------------------------
// Usage:
//   Workflow({ scriptPath: '.claude/workflows/doc-audit.js', args: {
//     doc:     '~/MainIdeas/Theories/CanvasControl.md',   // required
//     project: 'canvascurse',                             // required
//     seed:    'topics.md seed 1 — Kirby Canvas Curse AI', // optional; "none" is a valid answer
//   }})
//
// THIS PRODUCES FINDINGS, NOT EDITS. Theory documents are Tier 3 and read-only
// from these repos; a hook blocks writes to them. Drift is reported and logged
// as ledger rows, never fixed by rewriting.
// ---------------------------------------------------------------------------

const doc = args && args.doc
const project = (args && args.project) || 'unknown'
const seedHint = (args && args.seed) || null

if (!doc) throw new Error('doc-audit: args.doc is required — the path to the document to audit.')

const SEED_SCHEMA = {
  type: 'object',
  required: ['seedFound', 'stillAnswersIt', 'divergence', 'scale'],
  additionalProperties: false,
  properties: {
    seedFound: { type: 'string', description: 'which topics.md seed, or "none" with the reason' },
    stillAnswersIt: { type: 'string', enum: ['yes', 'partly', 'no', 'no-seed'] },
    divergence: { type: 'string', description: 'the specific question the document now answers instead' },
    scale: { type: 'string', description: "the seed's stated ambition versus the document's current one" },
  },
}

const VOCAB_SCHEMA = {
  type: 'object',
  required: ['seedTermsAbsent', 'docTermsNotInSeed', 'verdict'],
  additionalProperties: false,
  properties: {
    seedTermsAbsent: { type: 'array', items: { type: 'string' }, description: 'terms central to the seed with zero or near-zero occurrences in the document' },
    docTermsNotInSeed: { type: 'array', items: { type: 'string' }, description: 'load-bearing document vocabulary the seed never used' },
    counts: { type: 'string', description: 'the actual grep commands run and their counts' },
    verdict: { type: 'string' },
  },
}

const DIAGNOSIS_SCHEMA = {
  type: 'object',
  required: ['diagnoses'],
  additionalProperties: false,
  properties: {
    diagnoses: {
      type: 'array',
      items: {
        type: 'object',
        required: ['quote', 'where', 'actedOn'],
        additionalProperties: false,
        properties: {
          quote: { type: 'string' },
          where: { type: 'string', description: 'section, and how many document versions it has survived if determinable' },
          actedOn: { type: 'string', enum: ['yes', 'no', 'partly', 'unclear'] },
          note: { type: 'string' },
        },
      },
    },
    restatesPurpose: { type: 'string', description: 'does the document re-state why it exists past its opening section, and where' },
  },
}

const CHOICES_SCHEMA = {
  type: 'object',
  required: ['choices'],
  additionalProperties: false,
  properties: {
    choices: {
      type: 'array',
      items: {
        type: 'object',
        required: ['statement', 'where', 'kind', 'blastRadius', 'hasLedgerRow'],
        additionalProperties: false,
        properties: {
          statement: { type: 'string', description: 'the load-bearing statement, flatly' },
          where: { type: 'string' },
          kind: { type: 'string', enum: ['finding', 'choice'] },
          blastRadius: { type: 'string', description: 'factual: what depends on it. NOT a recommendation' },
          hasLedgerRow: { type: 'string', description: 'the existing DECISIONS_LEDGER row ID, or "none"' },
        },
      },
    },
  },
}

const seedLine = seedHint
  ? `The caller believes the seed is: ${seedHint}. Verify that rather than assuming it.`
  : `The caller did not name a seed. Determine it yourself. "No matching seed" is a legitimate result — three documents in this portfolio have none, and chaos-games descends from a seed it answers in a different field (ledger X-1b).`

const common = [
  `Document under audit: \`${doc}\``,
  `Project: ${project}`,
  `Seed file: \`~/MainIdeas/topics.md\` (four seeds; read it in full, it is short)`,
  `Ledger: \`~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md\``,
  ``,
  `Read \`docs/FAILURE-MODES.md\` F-9 first. Size is not the drift signal: CanvasControl.md is`,
  `1920 lines and did not drift; APC reached 805 and drifted badly. A document that keeps`,
  `saying why it exists does not drift; one that only says what it now is, does.`,
  ``,
  `Report findings only. Do not edit the document — it is Tier 3 and a hook blocks writes to it.`,
].join('\n')

phase('Probe')
log(`Auditing ${doc} against its seed (project: ${project})`)

const [seed, vocab, diagnosis, choices] = await parallel([
  () =>
    agent(
      [
        common,
        ``,
        `**Your probe: THE SEED TEST.**`,
        seedLine,
        ``,
        `Find the seed. Then answer, concretely: does the document still answer that question?`,
        `Compare the seed's stated ambition with the document's current one — seed 4 said`,
        `"probably a workshop paper in a smaller conference" and its document specified a`,
        `fourteen-month four-phase hardware programme. Neither is wrong alone; the DISTANCE is`,
        `the finding.`,
      ].join('\n'),
      { label: 'probe:seed', phase: 'Probe', schema: SEED_SCHEMA }
    ),
  () =>
    agent(
      [
        common,
        ``,
        `**Your probe: THE VOCABULARY TEST.**`,
        ``,
        `Build the term list from the SEED's vocabulary, not the document's. Then grep the`,
        `document for those terms and count. Report both directions: seed words the document`,
        `dropped, and load-bearing document words the seed never contained.`,
        ``,
        `This is how ledger row X-1b was established on 2026-08-17 — a grep for`,
        `robot|swarm|hazard|survival|sensor|environment|JAX|GPU returned zero on a document`,
        `descended from a robotics seed. Run actual greps and report the actual counts.`,
      ].join('\n'),
      { label: 'probe:vocabulary', phase: 'Probe', schema: VOCAB_SCHEMA }
    ),
  () =>
    agent(
      [
        common,
        ``,
        `**Your probe: UNADDRESSED SELF-DIAGNOSES.**`,
        ``,
        `A document that criticises itself and then continues unchanged has a defect invisible`,
        `to normal review — a confession does not look like a defect, so reviewers skip it.`,
        `CanvasControl.md's §1.2 substitution diagnosis survived FOUR versions.`,
        ``,
        `Grep for self-directed hedges: "a reviewer may", "worth checking whether", "we concede",`,
        `"this may be", "nothing changes", "this is the weakest", "may not be", "is not answered",`,
        `"and then not done". For every hit, trace it forward: was it acted on anywhere?`,
        ``,
        `Also answer: does the document re-state its own purpose anywhere PAST the opening`,
        `section? If §1 says why it exists and nothing after ever mentions it again, that is the`,
        `drift precondition regardless of the current content.`,
      ].join('\n'),
      { label: 'probe:self-diagnosis', phase: 'Probe', schema: DIAGNOSIS_SCHEMA }
    ),
  () =>
    agent(
      [
        common,
        ``,
        `**Your probe: THE CHOICE TEST.** This is the probe that actually prevents drift; the`,
        `others detect it after the fact.`,
        ``,
        `For every load-bearing statement in the document, classify it:`,
        `- **finding** — evidence forced it; it belongs in the document;`,
        `- **choice** — a different answer was available and would change downstream work.`,
        ``,
        `For every choice, check whether a DECISIONS_LEDGER.md row already exists for it and`,
        `give the row ID, or "none".`,
        ``,
        `blastRadius is a FACTUAL statement about what depends on the choice. It is NOT a`,
        `recommendation and must not contain one — the ledger's own header says the file`,
        `contains no recommendations, and that rule is the reason it works.`,
      ].join('\n'),
      { label: 'probe:choices', phase: 'Probe', schema: CHOICES_SCHEMA }
    ),
])

const unlogged = ((choices && choices.choices) || []).filter(
  (c) => c.kind === 'choice' && (!c.hasLedgerRow || c.hasLedgerRow.toLowerCase() === 'none')
)
const unaddressed = ((diagnosis && diagnosis.diagnoses) || []).filter((d) => d.actedOn === 'no')

log(`${unlogged.length} unlogged choices, ${unaddressed.length} unaddressed self-diagnoses`)

phase('Report')

const report = await agent(
  [
    `Assemble the drift report for \`${doc}\` from four independent probes. Format is in the`,
    `\`drift-check\` skill. Produce markdown only — do not edit anything.`,
    ``,
    `Probe results, as JSON:`,
    '```json',
    JSON.stringify({ seed, vocab, diagnosis, choices }, null, 2),
    '```',
    ``,
    `Produce two sections.`,
    ``,
    `**1. The drift report** — seed, still-answers-it, vocabulary both directions, scale,`,
    `unmarked choices, unaddressed self-diagnoses. State plainly where the probes disagree;`,
    `do not smooth it over.`,
    ``,
    `**2. Draft DECISIONS_LEDGER.md rows** for the ${unlogged.length} choices with no existing`,
    `row, in the ledger's table format:`,
    '`| ID | **choice, stated flatly** | where it lives | what changes if it changes | ☐ |`',
    ``,
    `Four rules on those rows, all load-bearing:`,
    `- **No recommendation.** The blast-radius column is factual.`,
    `- **The mark column stays ☐.** C / A / ? are his marks. Never fill one in.`,
    `- State each as a choice, not as an assumption the reader has to catch.`,
    `- Add **⚑** where the document already questions itself on that point.`,
    ``,
    `Do not write the rows into the ledger. Hand them over for review.`,
  ].join('\n'),
  { label: 'report', phase: 'Report' }
)

return {
  doc,
  project,
  seed,
  vocab,
  diagnosis,
  choices,
  unloggedChoiceCount: unlogged.length,
  unaddressedDiagnosisCount: unaddressed.length,
  report,
}
