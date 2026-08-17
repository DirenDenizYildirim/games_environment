# SURFACES — chaos-games

_The Tier 2 list. `PROTOCOL.md` §5.8. **Amending this list is itself Tier 2.**_

> **Provisional until code starts.** This list was written from the theory document before
> any implementation existed. Reviewing it is the first item of the first coding session —
> not because it is wrong, but because a surface list written from a document and one written
> from a codebase are different objects, and the gate should read the second.

The point of this file is that "Tier 2" is answered by lookup, not by judgment. *Is this
big?* is not the question. *Is it on the list?* is.

---

## Tier 2 surfaces

| Surface | Why it is Tier 2 | Named in |
|---|---|---|
| **The noise operator** — how execution noise is injected | The single most load-bearing object in Paper A. §9 Q1 asks whether uniform replacement is even the right null; changing it changes the μ(p) derivation and every threshold | Ledger **G-2**, theory §2.1–2.2 |
| **The skill ladder** — MCTS budget schedule | Defines what "strong player" means. All four thresholds are measured against it, and §5.6 flags it as an imperfect proxy | Ledger **G-3**, theory §1.2, §5.6 |
| **The divergence metric** — value space vs state space | Theorem-level for Paper B. §6.2 calls it "the second-most-likely point of attack" | Ledger **G-4**, theory §6.2 |
| **The FSLE estimator** | Paper B's central construct. The textbook Lyapunov exponent does not exist for a discrete game, so this is a constructed quantity, not a standard one | Ledger **G-9**, theory §6.3 |
| **The collapse-threshold estimator** — how `τ` is recovered from win-rate curves | It is the headline number. An estimator validated at a benign point is `FAILURE-MODES.md` F-8 | Theory §3 |
| **The game selection set** | 8–12 games with spread in `L`. No spread, no leverage in the headline regression — the result is decided here, before any run | Ledger **G-6**, theory §5.1 |
| **The statistics pipeline** — CI method, multiplicity correction, the regression | `PROTOCOL.md` §6: no silent statistical choices | Theory §5 |
| **The RNG / seeding path** | Determinism is a correctness property, not a convenience. Per-worker seeding passes every test you would write before failing silently | `CLAUDE.md` §4; theory §6.4 |
| **The run artifact schema** | Every run conforms. Mode (`explore`/`confirm`), seed, commit, prereg hash, and the search budget per condition all live here | `PROTOCOL.md` §7 |
| **The TAG interface layer** | The boundary to someone else's framework, on the JVM. §6.4's seed-discipline requirement may not be satisfiable inside TAG — that is a finding, and it changes the project if true | Ledger **G-7**, theory §5.1, §6.4 |

## Tier 3 additions beyond the standard set

| Trigger | Why |
|---|---|
| Changing **δ** (currently 0.05) | Sets M ≈ 785 per condition and therefore the whole compute budget. Ledger **G-11** |
| Making the **noise-aware / noise-blind** factor a robustness check instead of a headline factor | Halves the match count and removes `Δ_model`, which §5.4 calls possibly "the most citable thing in the paper." Ledger **G-10** |
| Introducing **human subjects** | Ethics approval is irreversible calendar. Ledger **G-5** currently rules it out and retitles around "skill expressibility" |
| Extending beyond **two players** | §9 Q3 says: either restrict explicitly or make it a contribution. Doing it by accident is neither. Ledger **G-8** |

## Explicitly NOT Tier 2

Without this table the list inflates until the gate becomes ritual and stops being read.

| Thing | Why it is fine to just do |
|---|---|
| Plotting, figures, tables, report formatting | Presentation. Wrong plots are visibly wrong |
| Logging, progress bars, CLI ergonomics, config file plumbing | Glue. Tests do not exist for it because nothing silent can go wrong |
| Adding a test for behaviour that already exists | Tier 0 explicitly. Never gate a new test |
| Refactors with no interface change and green tests | If the interface is unchanged and the tests are real, this is Tier 1 |
| Caching, batching, parallelism **that provably does not touch the RNG path** | Tier 1 — but "provably" means a determinism test across core counts, not an argument |
| Choosing which of the 8–12 selected games to run **first** | Ordering, not selection. The set is Tier 2; the order within it is not |
