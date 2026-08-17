# RISKS — canvascurse

_Live register. `PROTOCOL.md` §5.4. Statuses: `ACTIVE` · `WATCHING` · `MATERIALIZED` ·
`RETIRED` · `NOTED-OVERRIDDEN`._

Seeded 2026-08-17 from the theory document's own threat table, from `DECISIONS_LEDGER.md` §2,
and from the portfolio-level rows. The theory document's threat numbering (threat 1, 17, 18,
19) is preserved so the two can be read side by side.

---

| ID | Risk | Status | Trigger to watch | If it fires |
|---|---|---|---|---|
| **R-1** | **Scope.** ~3× over-scoped for 1 Mar 2027. Twelve milestones, six months of calendar, and ledger **C-7** — *"two papers, not one"* — stated in §9 and not done. | **ACTIVE** | It has already fired in assessment; it fires operationally at the first missed milestone | The scope cut is his decision. Until it is made, `BUDGET.md` cannot be filled in honestly and no schedule here is real |
| **R-2** | **`Π_ν` reads as a rescue knob** (theory threat 1). §2.5 says its absence in v1.0 was fatal; Q-5 asks the hostile version; a reviewer will ask it too. Every §5 result rests on it. | **ACTIVE** | Drafting §2.5 or any §5 result for external eyes | Ledger **C-2**, unmarked and load-bearing. Mitigation is an independent motivation for `Π_ν` that does not reference the v1.0 defect — if the only reason it exists is that the theory broke without it, the reviewer is right |
| **R-3** | **The §1.2 substitution still goes through** (theory threat 19). *"Swap the ball for a delivery drone and the ink for a beacon budget. Nothing in §2, §3 or §5 changes — not a symbol."* Four versions have not closed it. | **ACTIVE** | Any claim that this is a games paper | Ledger **C-1**. This is the venue question. v1.4 exists to answer it; whether it does has not been tested by anyone outside the document |
| **R-4** | **Related work cannot be written** until O-7 — the CoG/FDG/AIIDE 2019–2025 hand sweep — is run. Half a day, no substitute. | **ACTIVE** | Drafting §11 or any positioning claim | Blocking by construction. `SEARCH-PROTOCOL.md` §3 names it explicitly as not tool-substitutable |
| **R-5** | **No delta against robust / tube MPC** (theory threat 17, milestone M0b, item O-8). | **ACTIVE** | A control-literate reviewer, which at CoG is not guaranteed but is not unlikely either | One day of reading (Langson et al.; Majumdar & Tedrake) and a written §5.7 delta. Cheap now, expensive at review |
| **R-6** | **§5.9's machinery is standard beam optics** and §5.7 concedes it. A large share of §5's length carries a contribution that is only in the application. | **WATCHING** | Any artifact re-arguing novelty in §5.9 | Ledger **C-6**. Do not re-argue it — that is `FAILURE-MODES.md` F-7. If §5.9 is cut, it is the largest single scope saving available |
| **R-7** | **`c_tap > 0` contradicts strict "indirect control"** (theory threat 18), which is the genre premise the paper sells. | **WATCHING** | Framing the contribution around indirect control | Ledger **C-5**. Either the premise is stated with the tap channel included, or the tap channel is defended as part of the genre. Not both silently |
| **R-8** | **The solver is part of the measurement.** `ρ*` is defined by what a solver can certify, so a stronger solver lowers `ρ*` uniformly. Unequal solver strength across levels manufactures fake difficulty differences. | **WATCHING** | Any comparison across levels, or any solver upgrade mid-study | Same class as `chaos-robotics` CR-8 and as the parent project's optimizer-convergence risk. Equal budget per level, convergence diagnostics logged, invariance checked under a doubled budget on ≥1 level |
| **R-9** | **CoG rejects a dynamics paper wearing a games costume.** | **WATCHING** | Any §5 result with no `CanvasControl_GameDesign.md` §6 design image | The design-image rule is already built into the document. Enforce it — `PROTOCOL.md` §6, and the `redteam-designer` lens |
| **R-10** | **The α = 1 vs α = 2 contrast may not carry the primary figure.** §7.1 says the hyperbola alone is weak evidence. | **WATCHING** | Early results showing the two asymptotes are hard to separate | Ledger **C-8**. If it goes, the theoretical contribution goes with it and the paper becomes the benchmark alone — which may be the right paper anyway, and is C-7's other half |
| **R-11** | **Deferral becomes abandonment by default.** Standing advice is to defer this in favour of `chaos-games`; nothing in that advice says for how long. | **WATCHING** | Six months with no session on this project | Deferral should be a dated decision with a revisit condition, not an absence of activity. `PROTOCOL.md` §5.3's `Revisit if` field is the mechanism |

---

## Retired

_None._

## Overridden

_None._

---

_2026-08-17 — register created. Eleven risks seeded from the theory document's threat table,
the ledger and the portfolio. Nothing has fired; nothing has been retired._
