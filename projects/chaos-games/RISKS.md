# RISKS — chaos-games

_Live register. `PROTOCOL.md` §5.4. Statuses: `ACTIVE` · `WATCHING` · `MATERIALIZED` ·
`RETIRED` · `NOTED-OVERRIDDEN`._

Seeded 2026-08-17 from the theory document's own §9, from `DECISIONS_LEDGER.md` §3, and from
the portfolio-level rows. **A register that only grows is noise** — retire explicitly.

---

| ID | Risk | Status | Trigger to watch | If it fires |
|---|---|---|---|---|
| **R-1** | **No literature sweep has ever been run on this project.** | **PARTLY DISCHARGED** 2026-08-17 | The bounded K1 in `LITSEARCH-2026-08-17.md` | **K1 ran before any code.** The specific claim survives; three components did not (R-12…R-14). **But the run covered ~4% of its own term cross-product and traversed no forward citations**, so R-1 is not retired — it is narrowed. A full sweep is still owed before any novelty sentence |
| **R-12** | **The framing and the testbed are occupied.** Goodman, Perez-Liebana & Lucas, IEEE ToG 17(3):777–786 (2025), measure randomness's effect on outcome across **15 TAG games with an MCTS budget ladder** — same framework, same instrument class, same community, and they are the TAG authors. | **MATERIALIZED** (K1, 2026-08-17) | — | Already fired. Does not kill Paper A: they measure the spread from *inherent* randomness, not a collapse threshold, and make no length connection. But related work is now mandatory and specific, and no sentence may claim to be first here. Ledger **G-12**, three options, none marked |
| **R-13** | **The noise operator is a variant, not an invention.** Machado et al. (JAIR 2018) **sticky actions** is an established one-parameter, game-agnostic action-noise dial. §2.2's rejected-alternatives list does not mention it. | **MATERIALIZED** (K1, 2026-08-17) | — | Contribution (1) of Paper A as written overclaims. Add sticky actions to §2.2 and state the delta (uniform replacement vs action-repeat; threshold measurement vs robustness protocol). Ledger **G-13** |
| **R-14** | **Δ_model collides with determinization / strategy fusion.** Long, Sturtevant, Buro & Furtak (AAAI 2010) is precisely about an agent searching a model that does not match the true game. §5.4 calls Δ_model *"possibly the most citable thing in the paper"*; §8.2 cites no determinization work at all. | **MATERIALIZED** (K1, 2026-08-17) | — | **The largest unpatched hole K1 found.** Either Δ_model is repositioned against that literature or the claim is dropped to a measurement. Ledger **G-14** |
| **R-15** | **§6.8's `Σ > 0` hypothesis may have the sign backwards.** Goodman et al. report that *higher-budget agents better exploit different random seeds* — skill amplifies randomness's effect on outcome. §6.8 predicts skilled play suppresses amplification, treating `Σ < 0` as the rare memorable case. | **ACTIVE** | Any Paper B work on stabilization capacity | Different measurements, not a formal contradiction — but opposed in direction, on the same framework. Pilot `Σ` on two games before committing to the framing. Ledger **G-15** |
| **R-2** | **TAG may not ship 8–12 games with enough spread in `L`.** Ledger G-6 is stated as a selection criterion but rests on an unchecked fact about someone else's framework. | **ACTIVE** | O-12 completing | The headline regression loses leverage. Either widen the game set outside TAG (which reopens G-7) or the claim narrows |
| **R-3** | **The noise operator may be the wrong null.** §9 Q1 asks whether perturbation toward *plausible* actions is better than uniform replacement. | **ACTIVE** | A reviewer, or the μ(p) fit behaving badly | Changes the μ(p) derivation and every threshold. Ledger G-2, unmarked. Cheapest mitigation: run both on one game early |
| **R-4** | **MCTS budget-doubling may not be a defensible skill ladder.** §5.6 flags that it may not resemble how humans differ. | **ACTIVE** | Reviewer objection at CoG; or thresholds that move oddly with budget | All four thresholds are measured against it. Ledger G-3. Mitigation is framing (G-5's "skill expressibility" retitle) rather than a fix |
| **R-5** | **§6.2 (value-space divergence) and §6.3 (FSLE) are pre-flagged by the document as the attack surface.** The textbook Lyapunov exponent does not exist for a discrete game, so §6.3 is a construction, not a standard. | **ACTIVE** | Any artifact touching Paper B | Red-team required — `PROTOCOL.md` §3.3 triggers 1 and 2 both fire. §6.2 wants "a full defending paragraph" and does not have one |
| **R-6** | **Calendar.** Code starts Sept 2026 against a 1 Mar 2027 deadline; the document scopes at more than six months. Portfolio row X-2. | **ACTIVE** | The first slipped milestone | Cut to Paper A only. Ledger G-1 already says so, which makes this the cheapest cut in the portfolio |
| **R-7** | **CoG rejects a dynamics paper wearing a games costume.** The document says this itself in §0 and marks `[DESIGNER]` sections for the translation. | **WATCHING** | Any §6 or §7 result with no `[DESIGNER]` translation | Every formal object needs a design image. `PROTOCOL.md` §6, and the `redteam-designer` lens exists for it |
| **R-8** | **Paper B is started before Paper A**, because it is the more interesting one. | **WATCHING** | A session proposing §6 work before §3 is done | §7's link makes A the ground truth B is validated against. Running B first means validating against nothing |
| **R-9** | **Two-player restriction is neither committed to nor lifted.** §9 Q3 names both options and picks neither. | **WATCHING** | Any game selection including a >2-player game | Ledger G-8. It becomes a scope decision made by a game choice, which is F-9 |
| **R-10** | **δ = 0.05 gets treated as physics.** It sets M ≈ 785 and hence the compute budget, but it is a chosen threshold. | **WATCHING** | Any budget discussion quoting the match count as fixed | Ledger G-11. Any change to δ is a budget change and gets costed |
| **R-11** | **The "no human data" limitation may be over-stated**, which under-claims the paper. `CITATIONS.md` §5.1 — Isaksen et al. bridged simulated difficulty to >106M real sessions via a motor-skill player model. | **WATCHING** | Finalising §5.6 | Read Isaksen in the original first. Under-claiming is a smaller failure than over-claiming, but it is still a failure |

---

## Retired

_None._

## Overridden

_None._

---

_2026-08-17 — register created. Eleven risks seeded from the theory document, the ledger and
the portfolio._

_2026-08-17 — **K1 run** (`LITSEARCH-2026-08-17.md`). R-1 narrowed to PARTLY DISCHARGED.
**Three new risks materialized on paper rather than at review: R-12, R-13, R-14.** R-15 added
as ACTIVE. The specific `L^(−1/2)` claim survives, but the run was bounded and its `k = 0` on
that conjunction is provisional. Four draft ledger rows (G-12…G-15) await marking._
