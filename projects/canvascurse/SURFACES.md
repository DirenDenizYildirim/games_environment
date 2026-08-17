# SURFACES — canvascurse

_The Tier 2 list. `PROTOCOL.md` §5.8. **Amending this list is itself Tier 2.**_

> **Provisional until code starts.** Written from the theory document before any
> implementation existed. Reviewing it is the first item of the first coding session.

The point of this file is that "Tier 2" is answered by lookup, not by judgment.

---

## Tier 2 surfaces

| Surface | Why it is Tier 2 | Named in |
|---|---|---|
| **The ink model** — token bucket, regeneration rate, capacity | The theory document calls it *"the single most important modelling decision in the document."* Every result in §5, the window analysis, `β` and `R` all move with it | Ledger **C-4**, theory §2.3 |
| **The observation-noise channel `Π_ν`** | **Unresolved and load-bearing.** §2.5 says its absence in v1.0 was fatal; Q-5 asks whether it is a knob invented to rescue the theory; threat 1 says a reviewer will say so. Every §5 result rests on it | Ledger **C-2**, theory §2.5 |
| **The tap channel and `c_tap`** | Contradicts a strict reading of "indirect control," which the document concedes. Carries §5.8 and H5, and the whole path/velocity decomposition | Ledger **C-5**, theory §2.2 [P1] |
| **The `ρ*` estimator** | The headline quantity — the agent-free difficulty measure the paper is about. An estimator validated at a benign point is `FAILURE-MODES.md` F-8, and `ρ*` is a minimum, which makes benign points easy to pick by accident | Theory §4 |
| **The simulator core** — deterministic, all uncertainty epistemic | Ledger C-9 forces C-2 to exist at all. A stochastic simulator would supply uncertainty natively and change the framing of the whole paper | Ledger **C-9**, theory §2.1 |
| **The planner / solver** used to certify solvability at a budget | `ρ*` is defined by what a solver can achieve. A stronger solver lowers `ρ*` uniformly, so the solver is part of the measurement, not an implementation detail. This is the same gap as `chaos-robotics` CR-8 (`R*` is agent-free only *given* `F`) | Theory §4, §7 |
| **The level representation and the level set** | The benchmark half of the paper. What levels exist decides what the α = 1 vs α = 2 contrast can show | Ledger **C-7**, theory §9 |
| **The statistics pipeline** — CI method, multiplicity correction | `PROTOCOL.md` §6: no silent statistical choices | Theory §7 |
| **The RNG / seeding path** | The simulator is deterministic, which makes seeding *look* irrelevant — it is not: solver tie-breaking, level generation and any sampling still need a counter-based key | `CLAUDE.md` §4 |
| **The run artifact schema** | Mode, seed, commit, prereg hash, solver budget, realized ink consumption | `PROTOCOL.md` §7 |

## Tier 3 additions beyond the standard set

| Trigger | Why |
|---|---|
| Removing or replacing **`Π_ν`** | It is the document's only source of uncertainty. Removing it re-opens the v1.0 defect §2.5 calls fatal. Ledger **C-2** |
| Reverting the **§4 / §5 precedence** | v1.4's defining change. Reverting it is reverting to v1.3, and it changes the abstract, the track and the primary figure. Ledger **C-3** |
| Changing the **primary figure** away from the α = 1 vs α = 2 contrast | §7.1 says the hyperbola alone is weak evidence. If the contrast goes, the theoretical contribution goes with it. Ledger **C-8** |
| Splitting or merging the **theory/benchmark papers** | Ledger **C-7**. It is the scope decision the whole project waits on |
| Introducing **human subjects** or a playtest | Ethics approval is irreversible calendar. The document currently claims nothing that needs one |

## Explicitly NOT Tier 2

| Thing | Why it is fine to just do |
|---|---|
| Rendering, level visualisation, replay viewers | Presentation. This project needs them badly and none of them can be silently wrong |
| Plots, tables, report formatting | Same |
| Level *authoring* tools | Tooling. The level **set** is Tier 2; a faster way to build one is not |
| Logging, CLI, config plumbing | Glue |
| Adding a test for behaviour that already exists | Tier 0 explicitly |
| Refactors with no interface change and green tests | Tier 1 |
| Solver performance work that provably does not change which solutions are found | Tier 1 — "provably" means a test showing identical certified `ρ*` on a fixed level set, not an argument |
| Which levels to run **first** | Ordering, not selection |
