# chaos-games

_At what level of execution noise does a game stop separating strong players from weak ones —
and is that threshold predictable from the game's structure?_

| | |
|---|---|
| **Theory (authoritative)** | `~/MainIdeas/Theories/chaos-games-theory.md` (578 lines) |
| **Ledger** | `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` §3, rows G-1…G-11 |
| **Citations** | `~/MainIdeas/Supporting_Docs/CITATIONS.md` §3.2 |
| **Venue** | IEEE CoG 2027 — full papers **1 Mar 2027** |
| **Status** | **active.** No external gates. The CoG bet. |

## What it claims

Two papers, one underlying object.

**Paper A — *Skill Collapse Under Action Noise*.** Inject controlled execution noise into a
game and find the level at which it stops distinguishing skill. Claim: that threshold is
predictable from the game's structure, with a specific functional form.

**Paper B — *Chaos and Randomness Are Different Things and We Can Measure Both*.** Perturb
one decision and measure how fast the two futures diverge. Claim: that divergence rate is
separable from the game's stochasticity, is measurable, and predicts Paper A's threshold.

§7 derives the link — Paper B's divergence exponent appears inside Paper A's variance term.
That link is the cross-validation and, if it holds, the strongest single result.

**Order is fixed: A first.** A produces the ground truth B is validated against. Ledger
**G-1**: *"if you only write one, write A."*

## Why this one first

**It is the only project in the portfolio with no external gate.** No ethics approval, no
licence question, no paywalled blocking citation, no hardware, no counsel. Every other
project is waiting on someone or something. This one waits on nothing.

## What is already established

- **K1 ran 2026-08-17, before any code** — `LITSEARCH-2026-08-17.md`. All three active
  projects in the portfolio have now had a sweep before writing a line of code. The specific
  `L^(−1/2)` claim survives; the framing, the noise operator and Δ_model each have a named
  incumbent the document did not know about. The run was bounded — read §5 and §7 of the
  archive before quoting its `k`.
- The document answers `topics.md` **seed 2** — chaotic environments in *robotics* — in an
  entirely different field. Checked 2026-08-17: zero occurrences of *robot*, *swarm*,
  *hazard*, *survival*, *sensor*, *environment*, *JAX* or *GPU* (ledger **X-1b**). That
  transplant was not worthless: it turned *"barely trainable"* into `τ_skill` and *"is
  thinking worth anything"* into `τ_search`. But it means this document has **no seed of its
  own** in `topics.md`, which is the one condition `/drift-check` cannot check.
- `CITATIONS.md` §5.1 — Isaksen et al. validated simulated difficulty against **>106 million
  real play sessions** using a human motor-skill player model as a bridge. §5.6's limitation
  *"no human data, therefore no playability claims"* may be narrower than stated. Read it
  before finalising that section.

## What is blocked

Nothing. Two cheap desk items are open and neither blocks:

- **O-12** — TAG's current game roster and agent API (~1 hr). Worth doing before September:
  ledger **G-6** needs 8–12 games *with spread in `L`*, and whether TAG ships them is a fact,
  not an assumption.
- **O-9** — Palmer on predictability horizon; Kantz (1994) (~30 min).

## Where to start reading

1. `HANDOFF.md` here — always first.
2. Theory §0 (orientation, the two papers) and §1 (common formalism, notation).
3. Then the section the handoff names. **Do not read all 578 lines** — `PROTOCOL.md` §8.

§9 is the open-questions list and it is unusually honest; four of the eleven ledger rows are
flagged there by the document itself.
