# PORTFOLIO — Games_env

_Register of what this repo is building, against what deadline, behind which gates._
_Last reviewed: 2026-08-24 — the mandatory forward-citation sweep is **run**; the incumbent
turns out to be a research programme with a PhD thesis, not two papers; and §7.1 of the
`chaos-games` theory document is wrong in two compounding ways. See
`projects/chaos-games/LITSEARCH-2026-08-24.md` and `DERIVATION-2026-08-24.md`._

Read this at session start after the active project's `HANDOFF.md`. The handoff is
project-local truth; this file is what changed around it.

---

## 1. The calendar

| Venue | Event | Date | Status |
|---|---|---|---|
| IEEE CoG 2027 | Full paper deadline | **1 March 2027** | the binding date |
| IEEE CoG 2027 | Conference, University of Aizu | 2–5 August 2027 | — |

**Code starts September 2026.** That leaves roughly six months of calendar to the deadline,
against theory documents that scope at six to fourteen months of work. This is ledger row
**X-2** and it is the single largest portfolio-level risk in this repo. It is not solved by
working faster; it is solved by cutting scope, and the cut has to be a decision he makes.

---

## 2. Projects

### `chaos-games` — **active, no external gates**

*Skill collapse under action noise; chaos and randomness as separable measurables.*

Theory: `~/MainIdeas/Theories/chaos-games-theory.md` (578 lines)
Ledger: `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` §3, rows G-1…G-11
Citations: `CITATIONS.md` §3.2

Two papers, one object. **Paper A** (skill collapse) is written first and produces the
ground truth **Paper B** (divergence exponent) is validated against; §7 of the theory
document derives the link between them. Ledger row G-1: *"if you only write one, write A."*

**The one project with no external gate.** No ethics approval, no licence question, no
paywalled blocking citation, no hardware. It can start the day code starts. That is why it
is the CoG bet.

**K1 ran 2026-08-17, before any code** — `projects/chaos-games/LITSEARCH-2026-08-17.md`. The
specific `L^(−1/2)` claim survives; **the framing, the operator and Δ_model each turned out to
have a named incumbent the document did not know about** (Goodman/Perez-Liebana/Lucas ToG 2025
on TAG; Machado et al.'s sticky actions; Long et al. on strategy fusion). Risks R-12, R-13 and
R-14 materialized on paper rather than at review. The run was **bounded** — ~4% of the term
cross-product, no forward-citation sweep — so its `k = 0` is provisional and a full sweep is
still owed. Four draft ledger rows **G-12…G-15** await marking.

**2026-08-22 — the Goodman companion was extracted and read**
(`projects/chaos-games/READING-2026-08-22.md`). It **does** contain the length analysis the
ToG paper lacks: Figure 2 sweeps rounds-to-win in Love Letter and reports Trimmed Span
1.0 → 0.64. The `L^(−1/2)` claim **survives** — one game, a rule parameter, outcome *spread*
rather than a collapse *threshold*, no functional form fitted — but the qualitative
length–randomness relation is now published at CoG by the incumbent and may not be claimed
here. **R-14 narrowed:** Long et al. formalise no mismatch quantity, hold depth constant, and
are partly a *supporting* citation. **Two exposures no register held:** their §VI future work
*is* this project's question, in print (**R-16**); and **G-11's M ≈ 785 rests on a fixed-`p`
binomial the incumbent has published as inadequate and is currently correcting (R-17)**,
which puts the compute figure in `BUDGET.md` §1 under contest from outside. Three further
draft rows **G-16…G-18**, bringing the unwritten total to **seven**.

**2026-08-24 — the forward-citation sweep ran, and found more beside the targets than in
them** (`projects/chaos-games/LITSEARCH-2026-08-24.md`). **R-16 answers NO so far:** six
forward citations across both Goodman 2024/2025 papers, none taking up their printed §VI
question. The specific conjunction holds at `k = 0`; the broad `k` goes 12 → 16.

**But a third Goodman CoG 2024 paper exists that no register here held** — *Skill Depth in
Tabletop Board Games*, read in the original. It occupies the **skill-ladder** framing the way
the ToG paper occupies the randomness framing: 16 TAG games, MCTS budget ladder, and a fitted
three-parameter win-rate model whose `M` is a per-game skill-separation ceiling explicitly
attributed to stochasticity. `tabletopgames.ai` also lists a **2025 QMUL PhD thesis**
incorporating all of it, a **CoG 2026 paper on PIMC in imperfect-information games** (which
lands on `Δ_model`), and an **FDG 2023 paper on leader-following** (which lands on §3.4's `θ`).
**The exposure is a research programme, not two papers.** **R-18 added** — their own experiment
shows a small MCTS parameter shift lets a 32 ms agent beat a 1024 ms agent, which makes the
skill ladder's calibration per-game and parameter-dependent, and therefore a confound in the
headline regression. **R-14 re-opened**, **R-12/R-16 widened**, **R-17 gained a route** (the
thesis may hold the unpublished error-bound correction that gates `M ≈ 785`).

**Separately, a derivation check found §7.1 wrong twice** (`DERIVATION-2026-08-24.md`): it
substitutes a total over injection times into §3.2's per-decision variance slot, and its
integrand contradicts §6.2's own boundedness statement. **Correcting both restores the
`L^(−1/2)` law** — §7.1 as written implies the central claim fails in any game with appreciable
λ — while weakening the Paper A ↔ Paper B bridge from *exponential in λL* to *saturating in
λL*. Any edit following from this is Tier 3.

**Three further draft ledger rows G-19…G-21, bringing the unwritten total on this project to
ten.** `DECISIONS_LEDGER.md` §3 still ends at G-11.

Live tensions worth knowing before touching it:

- **G-2** — uniform action replacement as the noise operator. The theory document's own §9
  Q1 asks whether perturbing toward *plausible* actions is the better null, which would
  change the μ(p) derivation. Unmarked, large blast radius.
- **G-3** — MCTS budget-doubling as the skill ladder. §5.6 flags it as an imperfect proxy
  that may not resemble how humans differ. All four thresholds sit on it.
- **G-7** — TAG is the testbed, and TAG is JVM. The seed's *"JAX plus a rented 5090"* plan
  buys this project nothing. Do not import that plan from `topics.md`.
- **G-11** — δ = 0.05 sets M ≈ 785 matches per condition and therefore the whole compute
  budget. Any change to δ is a budget change.

Open desk items: **O-12** (TAG's current game roster and agent API, ~1 hr — worth doing
before September, since G-6's 8–12 games with spread in `L` depends on what TAG actually
ships) and **O-9** (Palmer on predictability horizon; Kantz 1994 — 30 min).

Not a correction but worth reading before finalising §5.6: `CITATIONS.md` §5.1. Isaksen et
al. validated simulated difficulty against >106 million real play sessions using a
motor-skill player model as the bridge. The document's "no human data, therefore no
playability claims" limitation may be narrower than it states.

### `canvascurse` — **active, over-scoped**

*Budgeted geometric actuation; `ρ*` as an agent-free level difficulty measure.*

Theory: `~/MainIdeas/Theories/CanvasControl.md` (1920 lines, v1.4 authoritative)
Companions: `Supporting_Docs/CanvasControl_{Formalization,LitReview,GameDesign}.md`
Ledger: `DECISIONS_LEDGER.md` §2, rows C-1…C-9
Citations: `CITATIONS.md` §3.3

The Kirby Canvas Curse reading of `topics.md` seed 1 — you control the pen, not the
character. **Assessed at roughly 3× over-scoped for a 1 March 2027 deadline.** The document
is sound; it is the scope that does not fit, and ledger row **C-7** is exactly this: *"two
papers, not one"* is stated in §9 and then not done.

Live tensions:

- **C-2** — observation noise `Π_ν` as the primary uncertainty channel. **Unresolved and
  load-bearing.** §2.5 says its absence in v1.0 "was fatal"; Q-5 asks whether it is "a knob
  invented to rescue the theory"; threat 1 says a reviewer may call it exactly that. Every
  result in §5 rests on it.
- **C-1** — venue is CoG, not a control venue. The document's own §1.2 diagnostic: *"Swap
  the ball for a delivery drone and the ink for a beacon budget. Nothing in §2, §3 or §5
  changes — not a symbol."* v1.4 exists to answer that, and §1.2 keeps re-stating it. That
  habit is why this document did not drift despite being the longest in the portfolio.
- **C-8** — the α = 1 vs α = 2 asymptote contrast is the primary figure. If it goes, the
  theoretical contribution goes with it.

Open desk items: **O-1** (Lemmings Builder step duration vs walk speed, <1 hr — play it or
read NeoLemmix/lix source), **O-7** (hand sweep of CoG/FDG/AIIDE 2019–2025 for
indirect-control papers, half a day, **blocks the related-work section**), **O-8** (robust
and tube MPC — Langson et al.; Majumdar & Tedrake — 1 day, and it is threat 17).

---

## 3. The standing recommendation, and its status

As of 2026-08-17 the portfolio ordering advice was: **`chaos-games` Paper A only, as the CoG
bet; defer `canvascurse`.** That is advice, not a decision, and it is not marked in the
ledger. Both projects are scaffolded here at equal depth so that deferring one stays a
reversible choice rather than a fact created by which directory has files in it.

If he reverses it, the first casualty is O-7 — half a day of literature work that blocks
`canvascurse`'s related-work section and has no substitute.

---

## 4. Cross-project constraints

| Constraint | Detail |
|---|---|
| **Shared nothing** | Unlike the robotics pair, these two projects share no simulator, no testbed and no claim. TAG is JVM; `canvascurse` needs a custom clone. There is no infrastructure economy in running both. |
| **No ROMs, no commercial assets, no decompilation** | `topics.md` ruled out Kirby ROMs for reproducibility. `CITATIONS.md` §1.4 records the Rain World project dying on exactly this. A reviewer must be able to run it. |
| **No human subjects currently planned** | If either project acquires one, that is Tier 3 *and* calendar-gated — ethics approval is irreversible lead time. `dda-axis`, not in this repo, is the portfolio's human-subjects project. |
| **Both are games papers** | Every formal object needs a design image. `PROTOCOL.md` §6. |

---

## 5. What would change this file

- A ledger row in §2 or §3 getting marked. **Seven are now drafted and unwritten on
  `chaos-games` alone** (G-12…G-18).
- CoG 2027 publishing a track list or a revised date.
- O-7 or O-12 completing.
- ~~The forward-citation sweep completing~~ — **run 2026-08-24.** What replaces it as a
  trigger: **the CoG/CIG 2019–2025 hand sweep**, which still has no open item on this project
  and which the sweep's own best retrieval argues for.
- **Goodman's 2025 PhD thesis being read** — it may resolve R-17 and therefore `BUDGET.md` §1.
- **Goodman et al. publishing their error-bound correction** — it lands directly on G-11,
  M ≈ 785 and therefore the whole compute budget (R-17).
- A decision on the §3 recommendation.
- Code starting, at which point `SURFACES.md` in each project becomes live rather than
  provisional.
