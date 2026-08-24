# RISKS — chaos-games

_Live register. `PROTOCOL.md` §5.4. Statuses: `ACTIVE` · `WATCHING` · `MATERIALIZED` ·
`RETIRED` · `NOTED-OVERRIDDEN`._

Seeded 2026-08-17 from the theory document's own §9, from `DECISIONS_LEDGER.md` §3, and from
the portfolio-level rows. **A register that only grows is noise** — retire explicitly.

---

| ID | Risk | Status | Trigger to watch | If it fires |
|---|---|---|---|---|
| **R-1** | **No literature sweep has ever been run on this project.** | **PARTLY DISCHARGED** 2026-08-24 | The bounded K1 in `LITSEARCH-2026-08-17.md` | **K1 ran before any code.** The specific claim survives; three components did not (R-12…R-14). **But the run covered ~4% of its own term cross-product and traversed no forward citations**, so R-1 is not retired — it is narrowed. **2026-08-24 — the forward pass is run** (`LITSEARCH-2026-08-24.md`) and the specific conjunction returned `k = 0` on **both** runs. The original risk — *no sweep has ever been run* — is **dead**. What remains, and should be read as the whole of R-1 from here: **term-exhaustion has not happened** (~4% of the cross-product) and **no CoG/CIG hand sweep exists**. Neither blocks code; both block a novelty sentence, which is a March deliverable |
| **R-15** | **§6.8's `Σ > 0` hypothesis may have the sign backwards.** Goodman et al. report that *higher-budget agents better exploit different random seeds* — skill amplifies randomness's effect on outcome. §6.8 predicts skilled play suppresses amplification, treating `Σ < 0` as the rare memorable case. | **ACTIVE — opposition real, severity lower than recorded** 2026-08-24 | Any Paper B work on stabilization capacity | **Provenance corrected 2026-08-24.** This row previously read *"Verified verbatim"* while `READING-2026-08-22.md` §3 simultaneously marked the source `[T]` — *"fetch-layer summary only."* A quote cannot be verbatim from a summary; that was `FAILURE-MODES.md` **F-1** sitting in the live register. **The paper has now been read in the original (`[V]`, `pdftotext`) and the sentence is genuine**, line 854: *"There is a clear pattern in all or most games for the effect of the random seed to increase as the skill of the players increases."* It was right by luck, not by process. **Two things the original shows that the register could not.** (a) **Their design is homogeneous agents** — same budget on both sides, Trimmed Span across five budgets, 200 observations per point. §6.8's `Σ = λ(π_random) − λ(π_strong)` compares **different** policies, so this differs in experimental design as well as in quantity, and the opposition is weaker than this row asserted. (b) **They name an unexplained counterexample.** Verbatim: *"Hearts. This is the game with the least visible trend for the impact of randomness to increase with skill. **This is unexpected**... The reason for this is not currently clear."* §6.8 says *"if you find even one such game, that is a memorable result and I would foreground it"* — **the incumbent has one, in print, unexplained.** Pilot `Σ` on two games and make **Hearts** one of them. Ledger **G-15** |
| **R-16** | **Our question is their declared future work.** Goodman et al. (CoG 2024) §VI states it in print: *"does greater skill increase or decrease the ability to mitigate stochasticity... Are there games for which randomness has a large effect on beginner players, but not for more skilled players?"* — the group that owns TAG, at the target venue, and the 2025 ToG paper already delivers part of it. | **WATCHING** 2026-08-24 | New forward citations appearing on either Goodman 2024/2025 paper | A declared research agenda from the incumbent is a clock. It is also an invitation, which cuts both ways — the framing is legitimate and the timing is not ours to control. Run the forward sweep before any novelty sentence. **2026-08-24 — forward sweep RUN** (`LITSEARCH-2026-08-24.md`). **Answer so far: nobody has taken the invitation** — six forward citations across both their 2024/2025 papers, none pursuing the §VI question. The clock is not stopped, but it has been read once |
| **R-17** | **The compute budget rests on a model the incumbent has published as inadequate.** G-11's δ = 0.05 → M ≈ 785 comes from a **fixed-`p` binomial**. Goodman et al. §VI: if `p` varies widely around a mean due to seed, *"more games need to be run for the same confidence interval... Calculating the correction required is current work in progress."* | **ACTIVE** | Any quotation of M ≈ 785, or the ~10⁶-match figure | Hits statistics and budget at once, and the condition they describe is the one this project studies. Their correction is unpublished, so it cannot be adopted yet — but M ≈ 785 may be an underestimate and `BUDGET.md` §1 derives everything from it. Ledger **G-18**; any change to M is a budget change. **2026-08-24 — a route may exist.** Goodman's 2025 PhD thesis *incorporates* these papers, and a thesis is where work-in-progress lands before separate publication. Reading it may resolve `M ≈ 785` without waiting on a journal |
| **R-18** | **The skill ladder's calibration is an artifact of MCTS parameter choice — and the incumbent published the demonstration.** Goodman, Perez-Liebana & Lucas, *Skill Depth in Tabletop Board Games*, **CoG 2024** §VII-A: *"A small shift in MCTS parameter space gives a better policy that with a 32ms budget can easily defeat a Classic 1024ms agent."* They also report that per-game tuning *"makes a significant change in the rating of some games."* | **ACTIVE — CONFIRMED, three axes** 2026-08-24 | Any cross-game threshold comparison — i.e. the headline regression itself | §1.2's stated safeguard is that `W_0` be **monotone in `j`**, and it will be — budget-monotonicity is not the property at risk. What is: the same budget ratio buys **different amounts of skill in different games**, depending on where default MCTS parameters sit for that game. `SURFACES.md` states all four thresholds are measured against the ladder, and §5.2 compares them **across** games, so this is a per-game confound in `β₁` that the three predictors cannot absorb. Mitigation is ledger **G-20**, and **every option there is a budget change** — their tuning uses **NTBEA**, a per-game optimisation run `BUDGET.md` does not cost. **CONFIRMED same day** by §VI: *"Optimal settings may vary both by player count and the computational budget… **For some games it was found that the same agent was robustly best across all player counts and budgets, while for others this varied.**"* Heterogeneous across games — a confound, not a uniform limitation. **Widened from one axis to three:** MCTS parameters (Skill Depth §VI, 8 tunable dimensions), **information-handling algorithm** (PIMC CoG 2026 — *"varies by game"*; PI-MCTS worse than baseline in 4 of 12), and **objective function / rollout length** (Following the Leader, FDG 2023). §1.2 fixes one dimension of a space the incumbent tunes in eight. `READING-2026-08-24.md` |
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

**Retired 2026-08-24 — discharged into writing obligations.** These three stopped being risks
once their deltas were established. Each is now *a citation the paper must make and a sentence
it must contain* — a drafting task, not an uncertain future event. **Retiring them is not
retracting them:** the obligations below are binding, and the evidence stays in
`LITSEARCH-2026-08-17.md`, `READING-2026-08-22.md` and `READING-2026-08-24.md`.

| ID | What remains as a binding obligation |
|---|---|
| **R-12** | §8.2 must cite Goodman/Perez-Liebana/Lucas — ToG 2025 **and both** CoG 2024 papers — and state the delta in one sentence: *they measure the spread produced by a game's own randomness; we inject a dial and locate where skill stops registering, as a function of length.* **No sentence may claim to be first here.** Ledger **G-12** |
| **R-13** | §2.2's rejected-alternatives list must name **sticky actions** (Machado et al., JAIR 2018) and state the delta: `ς` is fixed at 0.25, never swept, and tied to neither skill separation nor episode length. Contribution (1) must not be worded as inventing a noise dial. Ledger **G-13**. **Still `[T]`** — the sentence itself needs the original |
| **R-14** | §8.2 must cite determinization / strategy-fusion work (Long et al. 2010; Ravichandran/Goodman/Lucas CoG 2026). **`Δ_model` survives as a headline factor** — read twice, neither formalises a model-mismatch quantity. Ledger **G-16** |

_Rows preserved verbatim for provenance:_

| ID | Risk | Status | Trigger | If it fires |
|---|---|---|---|---|
| **R-12** | **The framing and the testbed are occupied.** Goodman, Perez-Liebana & Lucas, IEEE ToG 17(3):777–786 (2025), measure randomness's effect on outcome across **15 TAG games with an MCTS budget ladder** — same framework, same instrument class, same community, and they are the TAG authors. | **MATERIALIZED** (K1, 2026-08-17) | — | Already fired. Does not kill Paper A: they measure the spread from *inherent* randomness, not a collapse threshold, and make no length connection. But related work is now mandatory and specific, and no sentence may claim to be first here. Ledger **G-12**, three options, none marked. **2026-08-24 — widened.** The exposure is a **research programme with a PhD thesis**, not two papers: `tabletopgames.ai` lists a 2025 QMUL thesis plus ≥6 relevant papers, of which this register held one. See **R-18** and `LITSEARCH-2026-08-24.md` §1.1 |
| **R-13** | **The noise operator is a variant, not an invention.** Machado et al. (JAIR 2018) **sticky actions** is an established one-parameter, game-agnostic action-noise dial. §2.2's rejected-alternatives list does not mention it. | **MATERIALIZED, delta established** 2026-08-22 | — | Contribution (1) as written still overclaims, but the delta is clean: ς is **fixed at 0.25 and never swept**, its stated purpose is separating brittle open-loop from robust closed-loop policies, and it is connected to **neither skill separation nor episode length**. Uniform replacement swept across `p` to locate a threshold and predict it from `L` is a different instrument. Add to §2.2 and state that. Ledger **G-13**. **Read at `[T]` only — the sentence itself needs the original** |
| **R-14** | **Δ_model collides with determinization / strategy fusion.** Long, Sturtevant, Buro & Furtak (AAAI 2010) is precisely about an agent searching a model that does not match the true game. §5.4 calls Δ_model *"possibly the most citable thing in the paper"*; §8.2 cites no determinization work at all. | **NARROWED (again)** 2026-08-24 | — | **Read in the original** (`READING-2026-08-22.md` §5). Smaller than K1 judged: they formalise **no** model-mismatch quantity, inject no noise, use no skill ladder, and **hold tree depth constant at 8**. Their mismatch is *informational*; Δ_model is *execution-noise*. They are also a **supporting** citation — they establish that structural properties predict when a mismatch causes loss, which is this project's argument form. §8.2 must cite them; Δ_model need not drop to a measurement. Ledger **G-16**, a third option G-14 does not list. **2026-08-24 — re-opened.** The 2010-based narrowing reasoning is untouched, but **Ravichandran, Goodman & Lucas have a CoG 2026 paper evaluating PIMC in imperfect-information games** — the incumbent, at the target venue, in the current cycle, on the exact mechanism `Δ_model` measures. **2026-08-24 — READ (`[V-sub]`), and it narrows again.** It is an **algorithm comparison** (PI-MCTS vs OL-MCTS vs IS-MCTS, twelve TAG games), not a formalisation: **no model-mismatch quantity, no injected noise, no skill ladder as instrument.** `Δ_model` **survives** and §5.4 may keep it. R-14 returns to what it has been since 2026-08-22 — a **related-work obligation**, not a threat. Its per-game algorithm sensitivity instead feeds **R-18** |


## Overridden

_None._

---

_2026-08-17 — register created. Eleven risks seeded from the theory document, the ledger and
the portfolio._

_2026-08-17 — **K1 run** (`LITSEARCH-2026-08-17.md`). R-1 narrowed to PARTLY DISCHARGED.
**Three new risks materialized on paper rather than at review: R-12, R-13, R-14.** R-15 added
as ACTIVE. The specific `L^(−1/2)` claim survives, but the run was bounded and its `k = 0` on
that conjunction is provisional. Four draft ledger rows (G-12…G-15) await marking._

_2026-08-22 — **the Goodman companion was extracted and read** (`READING-2026-08-22.md`);
fetching it to disk and running `pdftotext` works where the earlier attempt failed. **It
contains the length analysis.** `L^(−1/2)` survives — one game, a rule parameter, outcome
spread rather than a threshold, no functional form fitted — but the qualitative
length–randomness relation is now published at CoG by the incumbent and may not be claimed.
**R-14 narrowed** (Long et al. read in full: no mismatch quantity, depth held constant, and
they are partly a supporting citation). **R-13's delta established.** **R-15 confirmed
opposed** on the record. **Two risks added that no register held: R-16** — our question is
their printed future work — **and R-17** — G-11's M ≈ 785 rests on a fixed-`p` binomial the
incumbent has published as inadequate and is currently correcting. Three draft ledger rows
**G-16, G-17, G-18** await marking, alongside the still-unwritten G-12…G-15._

_2026-08-24 — **the mandatory forward-citation sweep was run** (`LITSEARCH-2026-08-24.md`) and
a derivation check was run against the theory document (`DERIVATION-2026-08-24.md`).
**R-16's question answers NO so far** — six forward citations across both Goodman 2024/2025
papers, none taking up their §VI invitation, and the specific conjunction stays at `k = 0`.
**R-18 added as ACTIVE**: a third Goodman CoG 2024 paper — *Skill Depth in Tabletop Board
Games*, held by no register here and read in the original — demonstrates that a small shift in
MCTS parameter space lets a 32 ms agent beat a 1024 ms agent, which makes the skill ladder's
calibration per-game and parameter-dependent. **R-14 re-opened** on a CoG 2026 PIMC paper from
the incumbent. **R-12 and R-16 widened** — the exposure is a research programme with a PhD
thesis, not two papers. **R-17 gained a route** — that thesis may contain the error-bound
correction. Three draft ledger rows **G-19, G-20, G-21** await marking, bringing the unwritten
total to **ten**._

_2026-08-24 (second entry) — **three Block A reads completed** (`READING-2026-08-24.md`).
**R-18 confirmed and widened to three axes** — the incumbent publishes per-game variation in
MCTS parameters, information-handling algorithm, and objective function; §VI's *"for others
this varied"* is what turns it from a limitation into a confound in `β₁`. **R-14 narrowed
again** — the CoG 2026 PIMC paper formalises no mismatch quantity, so `Δ_model` survives.
**A title-based inference was corrected:** *Following the Leader* (FDG 2023) is about agent
objective functions, **not** about game feedback structure, and does **not** bear on §3.4's
`θ`, which remains unoccupied. **R-17 unresolved** — the thesis is network-blocked from this
machine — but §1.3 gives the budget's *feasibility* half its first external comparator._

_2026-08-24 (third entry) — **register hygiene pass, before code starts.** **R-12, R-13 and
R-14 retired** into binding writing obligations — each had resolved to *cite them and state the
delta*, which is a drafting task, not an uncertain event. **R-16 downgraded to WATCHING** (the
forward sweep ran and came back clean). **R-1 restated** — *no sweep has ever been run* is dead;
what remains is term-exhaustion and the CoG/CIG hand sweep, neither of which blocks code.
**R-15's provenance corrected** — it read *"Verified verbatim"* on a `[T]` source for two days;
the source has now been read in the original and the quote is genuine, but the severity is lower
than recorded and **Hearts** is added as a named `Σ < 0` candidate. **Live rows: 18 → 15**, of
which the ones that gate work before March are **R-17, R-18, R-2, R-3, R-4, R-5, R-6**._
