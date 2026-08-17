# HANDOFF — chaos-games
_Last session: 2026-08-17 | no repo history yet | K1 run_

## Current state

Theory document complete at 578 lines, v0.1, two papers scoped. Eleven original ledger rows,
**none marked**; four new ones drafted and unwritten. No code, no preregistration.

**K1 ran 2026-08-17, before any code** — `LITSEARCH-2026-08-17.md`. This project is no longer
the one with zero external contact.

**The specific claim survives.** Nothing retrieved does the conjunction: inject a one-parameter
execution-noise dial → locate where a skill ladder stops separating → predict that threshold
from match length with a derived exponent. `β₁ = −1/2` appears unoccupied.

**Three components did not survive intact:**

- **The framing and testbed are occupied.** Goodman, Perez-Liebana & Lucas, IEEE ToG
  17(3):777–786 (2025) — 15 TAG games, MCTS budget ladder, measuring how randomness determines
  outcome. Same framework, same community, and they are the TAG authors.
- **The noise operator is a variant.** Machado et al.'s **sticky actions** (JAIR 2018) is an
  established one-parameter game-agnostic action-noise dial. §2.2 does not mention it.
- **Δ_model collides with determinization / strategy fusion** (Long, Sturtevant, Buro & Furtak,
  AAAI 2010). §5.4 calls it possibly the most citable thing in the paper; §8.2 cites none of
  that literature. **This is the largest unpatched hole.**

**The run was bounded** — ~16 queries against a cross-product of 400+, and **no forward-citation
sweep**, which `SEARCH-PROTOCOL.md` §3 makes mandatory. The `k = 0` on the specific conjunction
is therefore provisional. What K1 actually established is the three collisions above.

## In flight

Nothing half-built. `LITSEARCH-2026-08-17.md` is written and closed — it is not to be edited;
a second run is a second file.

Four ledger rows **G-12…G-15** are drafted in that file's §6 and **have not been written to
`DECISIONS_LEDGER.md`**. That is the next mechanical step and it needs his go-ahead, since it
touches a portfolio-wide file.

## Blocked

Nothing hard-blocked. One thing is now conditionally blocked:

- **Any novelty sentence for Paper A** should wait on the full sweep. The bounded run supports
  "no prior work does X" only weakly, and `FAILURE-MODES.md` F-1 is exactly this failure.

## Next actions

Ordered.

1. **Append G-12…G-15 to `DECISIONS_LEDGER.md` §3** — drafted in `LITSEARCH-2026-08-17.md` §6,
   unmarked, no recommendations. Needs his go-ahead.
2. **Read Goodman, Perez-Liebana & Lucas in the original** (arXiv:2503.02686 / ToG 17(3)).
   Currently `[V-sub]` via an HTML fetch. It is the nearest work and the delta sentence cannot
   be written from a summary. ~1 hr. **Also fetch its companion**, *Measuring Randomness in
   Tabletop Games* (Goodman 2024) — the PDF would not extract and it may contain the length
   analysis the ToG paper lacks.
3. **Run the forward-citation sweep** on retrievals 1, 2 and 5. Mandatory under
   `SEARCH-PROTOCOL.md` §3 and skipped in this run.
4. **Complete the term cross-product** — `/litsweep`, or `.claude/workflows/litsweep.js` with
   `maxSlices` raised. This run covered roughly 4% of it.
5. **O-12 — TAG's roster and agent API** (~1 hr). Unchanged in priority, and now doubly
   relevant: G-12 option (c) is "change testbed", and that decision needs to know what TAG has.
6. **O-9 — Palmer, Kantz** (~30 min). Unchanged.

## Open questions

His. Original rows first, then what K1 raised.

- **G-2** — uniform action replacement as the null. **K1 added a third option nobody had
  considered: do not inject at all, control the seed**, which is Goodman et al.'s instrument.
- **G-3** — MCTS budget-doubling as the skill ladder. Note Goodman et al. use the same
  mechanism, which is corroboration for its acceptability at this venue.
- **G-8** — two-player only, still neither committed to nor lifted.
- **G-11** — δ = 0.05, sets M ≈ 785 and the whole compute budget.
- **G-12** — how to position against Goodman et al. Three options, none marked.
- **G-13** — is the noise operator claimed as novel, given sticky actions.
- **G-14** — is Δ_model claimed as new, given determinization.
- **G-15** — does §6.8's `Σ > 0` survive Goodman et al.'s opposite-direction finding.

## Traps for next session

- **`LITSEARCH-2026-08-17.md` is write-once.** Do not edit it to add later findings. A second
  run is a second file.
- **Do not quote `k = 0` as a novelty result.** The run covered ~4% of its term cross-product
  and ran no forward-citation sweep. The file says so in §5 and §7; keep it that way.
- **Ten of fourteen retrievals are `[T]`** — not read in the original. None may carry a novelty
  claim at that tier.
- **TAG is JVM.** Unchanged: `topics.md`'s JAX-and-a-rented-5090 plan belongs to the robotics
  seed. Ledger **G-7**.
- **This document has no seed of its own** in `topics.md`; it descends from seed 2, which asked
  a robotics question. Ledger **X-1b**. `/drift-check` will find no matching seed — known, not
  a bug.
- **Paper B started before Paper A** remains the sequencing trap. §7's derivation makes A the
  ground truth B is validated against.
- **§6.8's sign may be wrong.** Pilot `Σ` on two games before building the framing around
  `Σ > 0`.
