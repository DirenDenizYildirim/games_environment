# LITSEARCH — chaos-games — 2026-08-17

**Claim under test (Paper A, theory §3.3):** the execution-noise level at which a game stops
distinguishing strong from weak players is predictable from the game's structure, with the
noise-tolerance gap decaying as `1 − τ_skill ∝ L^(−1/2)` in decisions per player per match.

**Upper cutoff:** 2026-08-17. Anything published after this date is out of scope for this run
and triggers a fresh run rather than an amendment.
**Protocol:** `docs/SEARCH-PROTOCOL.md`, as written 2026-08-17.
**Run by:** Claude, in-session, no subagents. **Bounded run — see §5.**

---

## 1. Result

> **Broad question — `k = 12`, tier `[T]`/`[V-sub]` mixed.** Twelve retrieved works ask some
> version of *"how much of a game's outcome is skill versus chance, and how does that interact
> with agent strength."*
>
> **Specific conjunction — `k = 0`, over the surface reached.** No retrieved work injects a
> controlled one-parameter execution-noise dial, measures the threshold at which a skill
> ladder stops separating, **and** predicts that threshold from match length with a derived
> exponent.

**Nearest work — two, for different halves of the claim:**

**(a) For the instrument and the community:** Goodman, Perez-Liebana & Lucas, *"Seeding for
Success: Skill and Stochasticity in Tabletop Games"*, **IEEE Transactions on Games 17(3):
777–786 (2025)**, arXiv:2503.02686. **Same framework (TAG), same skill ladder mechanism (MCTS
budget), 15 tabletop games, same community — these are the TAG authors.**

*Differs in:* they exploit **inherent** randomness by controlling seeds (200 seeds × 1000
games) rather than injecting a noise parameter; they measure the **spread** of win rates
(entropy, span, trimmed span, outlier fraction) rather than a **collapse threshold**; and they
make **no connection to game length** and derive no scaling law.

**(b) For the scaling law:** Ben-Naim, Vazquez & Redner, *"Parity and Predictability of
Competitions"*, **Journal of Quantitative Analysis in Sports 2(4) (2006)**. Upset probability
`q` as a one-parameter randomness dial; explicitly derives that the standard deviation of the
winning fraction is **inversely proportional to the square root of the number of games played**,
with `σ = (1/2 − q)/√3` in the long-season limit.

*Differs in:* `q` is estimated from sports data, not injected; length means **games per
season**, not **decisions per match**; and no threshold at which skill ceases to register is
defined.

---

## 2. Exact queries issued

All via WebSearch unless marked. Index: general web + arXiv + Semantic Scholar surfacing.

1. `measuring skill and chance in games noise threshold win rate`
2. `number of games required to determine better player upset probability parity competitions`
3. `Jaffe restricted play evaluating competitive game balance AIIDE`
4. `game length skill luck ratio match length stronger player wins square root`
5. `arXiv "Luck, skill, and depth of competition" games social hierarchies preprint`
6. `sticky actions stochasticity Arcade Learning Environment Machado action noise agent evaluation`
7. `Lyapunov exponent board game state divergence perturbation chaos measure game trees`
8. `how much randomness before skill stops mattering game design threshold agent win rate noise sweep`
9. `Browne Maire evolutionary game design quality metrics drama uncertainty depth measure`
10. `Tabletop Games framework TAG skill stochasticity MCTS budget win rate randomness Gaina Goodman`
11. `"skill depth" OR "skill expression" game measure injecting noise agent strength collapse CoG IEEE conference games`
12. `"Seeding for Success" Goodman skill stochasticity tabletop games cited by follow-up 2025 2026`
13. `perfect information Monte Carlo determinization agent wrong model of stochasticity strategy fusion Long Sturtevant`
14. `"finite-size Lyapunov exponent" OR "prediction horizon" applied to games gameplay turns designer metric`
15. `game length number of decisions predicts skill differentiation scaling exponent tabletop games regression empirical`
16. `rubber banding catch-up mechanics snowballing effect on skill expression measured formal model games`

Full-text fetches attempted (WebFetch):
`science.org/doi/10.1126/sciadv.adn2654` (**403**) · `cnls.lanl.gov/~ebn/pubs/sports-jqas/sports-jqas.pdf`
(**binary, no extraction**) · `cnls.lanl.gov/~ebn/pubs/sports/html/` (**OK**) ·
`arxiv.org/html/2503.02686` (**OK**) · `arxiv.org/abs/2312.04711` (**abstract only**) ·
`tabletopgames.ai/assets/pdf/Goodman2024RandomAnalysis.pdf` (**binary, no extraction**) ·
`arxiv.org/html/2410.14363` (**OK**) · `uni-trier.de/.../duersch--Skill_and_chance_2018-03-07.pdf`
(**binary, no extraction**)

---

## 3. Retrievals

| # | Work | Tier | Counts toward k | Why / setting mismatch |
|---|---|---|---|---|
| 1 | Goodman, Perez-Liebana & Lucas, *Seeding for Success: Skill and Stochasticity in Tabletop Games*, IEEE ToG 17(3):777–786, 2025 (arXiv:2503.02686) | **[V-sub]** | **yes** | **Nearest work.** TAG, 15 games, MCTS budget ladder (0/2/10/50/250 ms). Seed-controlled inherent randomness, not injected noise. No threshold, no length scaling |
| 2 | Ben-Naim, Vazquez & Redner, *Parity and Predictability of Competitions*, JQAS 2(4), 2006 | **[V-sub]** | **yes** | **Nearest work for the exponent.** Upset probability `q`; σ ∝ 1/√(games); `σ=(1/2−q)/√3`. Sports, season length, no collapse threshold |
| 3 | Jerdee & Newman, *Luck, skill, and depth of competition in games and social hierarchies*, Science Advances 10:eadn2654, 2024 (arXiv:2312.04711) | **[T]** | **yes** | Luck (upset) + depth parameters **inferred from win–loss records**. No injection, no length dependence located. **Full text not read — see §5** |
| 4 | Duersch, Lambrecht & Oechssler, *Measuring skill and chance in games*, European Economic Review, 2020 | **[T]** | **yes** | Elo-spread measure; "critical repetition frequency" — ~750 poker hands for skill to dominate chance. **A repetitions-to-dominance threshold**, but over whole-game repetitions, not within-match decisions; no injected noise |
| 5 | Jaffe, Miller, Andersen, Liu, Karlin & Popović, *Evaluating Competitive Game Balance with Restricted Play*, AIIDE 2012 (Best Student Paper) | **[T]** | **yes** | Restricted agents vs standard agents — structurally the same instrument as noising the control channel. Capability handicap, not stochastic noise; balance, not skill collapse |
| 6 | Machado, Bellemare, Talvitie, Veness, Hausknecht & Bowling, *Revisiting the Arcade Learning Environment*, JAIR 61, 2018 (arXiv:1709.06009) | **[T]** | **yes** | **Sticky actions:** a one-parameter, game-agnostic action-noise operator, now standard for robustness evaluation. Action-repeat rather than uniform replacement; used as an evaluation protocol, not to locate a threshold |
| 7 | Browne & Maire, *Evolutionary Game Design* (Ludi), IEEE TCIAIG 2010 / Springer 2011 | **[T]** | **yes** | "Drama" and "uncertainty" quality metrics; robustness to random and obstructive players. Outcome-uncertainty measures without an injected dial |
| 8 | Liu, Togelius, Perez-Liebana & Lucas, *Evolving Game Skill-Depth using General Video Game AI Agents*, IEEE CEC 2017 (arXiv:1703.06275) | **[T]** | **yes** | Skill-depth from agent-strength differences; explicitly handles resampling against noise. GVGAI, evolution of games rather than measurement of existing ones |
| 9 | *Quickly Detecting Skill Trace in Games*, IEEE CoG 2022 | **[T]** | **yes** | "Skill trace" — a game's potential for tactical/strategic interest, detected quickly. Title/abstract only |
| 10 | Banerjee, De, Maitra & Mukherjee, *Skill vs. Chance Quantification and Relative Ranking for Popular Card & Board Games*, arXiv:2410.14363, 2024/2025 | **[V-sub]** | **yes** | Regression of win rate on player experience, real player data (Chess, Rummy, Ludo, Teen Patti). No agents, no injection, no scaling law |
| 11 | *Quantifying Skill and Chance: A Unified Framework for the Geometry of Games*, arXiv:2511.11611, 2025 | **[T]** | **yes** | Skill/chance as complementary control over stochastic decision trees. **Title and one-line description only** |
| 12 | Lantz, Isaksen, Jaffe, Nealen & Togelius, depth / skill-chain work on strategic games | **[T]** | **yes** | Skill chains — longest sequence of players each beating the next at ~60%. A discrete cousin of τ_rank. Surfaced via secondary description, not read |
| 13 | Long, Sturtevant, Buro & Furtak, *Understanding the Success of Perfect Information Monte Carlo Sampling in Game Tree Search*, AAAI 2010 | **[T]** | **no** | Does not ask the headline question. **Recorded because it is a related-work obligation the theory document does not list — see §4.3** |
| 14 | Isaksen, Gopstein, Togelius & Nealen, game-space parameter sweeps (Flappy Bird) | **[T]** | **no** | Methodological precedent for sweeping a game parameter and measuring outcome; already named in theory §8.2. Not a skill-collapse measurement |

---

## 4. Findings

### 4.1 The specific claim survives

Nothing retrieved does the conjunction: **inject a one-parameter execution-noise dial → locate
the threshold where a skill ladder stops separating → predict that threshold from match length
with a derived exponent.** Paper A's `β₁ = −1/2` regression appears unoccupied over the surface
reached. `k = 0` here is a **weak** result — it is the absence of evidence against novelty over
a bounded surface, not evidence of novelty. Read it against §5.

### 4.2 The framing and the testbed are occupied

**Goodman, Perez-Liebana & Lucas (ToG 2025) is on TAG, uses an MCTS budget ladder, covers 15
tabletop games, and asks how randomness determines outcome.** They are the TAG authors and the
target community. This does not kill Paper A, but it means:

- Related work is **mandatory and specific**, not a citation. The paper must state the delta in
  one sentence: *they measure the spread produced by a game's own randomness; we inject a dial
  and locate where skill stops registering, as a function of length.*
- Any sentence claiming to be first to measure how randomness affects skill in tabletop games
  is false as written.
- Their instrument is a genuine alternative to the noise operator, and ledger row **G-2**
  (uniform replacement as the null) now has a third option nobody has considered: *do not
  inject at all — control the seed*.

### 4.3 Three components are less novel than the document treats them

- **The √L mechanism is not new.** Ben-Naim/Redner have σ ∝ 1/√(games) since 2006, and it is
  the CLT. Theory §3.1 already calls it "the folk result", which is correct and should stay —
  but §3.3's headline must claim the **noise-tolerance threshold's** `L^(−1/2)` decay, not the
  √L skill scaling itself. That distinction is currently clear in the maths and blurry in the
  prose.
- **The noise operator is a variant, not an invention.** Machado et al.'s **sticky actions** is
  already a one-parameter, game-agnostic action-noise dial in standard use. §2.2 lists three
  rejected alternatives and does not mention it. A reviewer from the RL side will.
- **Δ_model collides with a literature the document does not cite.** Noise-aware vs noise-blind
  is an agent searching a model that does not match the true game — which is exactly
  **strategy fusion / determinization** (Long, Sturtevant, Buro & Furtak 2010; Whitehouse,
  Powley & Cowling on ISMCTS). §5.4 calls Δ_model *"possibly the most citable thing in the
  paper"*; §8.2's related-work list contains no determinization work at all. **This is the
  largest unpatched hole this sweep found.**

### 4.4 One empirical finding points against a stated prediction

Goodman et al. report that **higher-budget (more skilled) agents better exploit the benefit of
different random seeds** — skill *amplifies* the effect of randomness on outcome.

Theory §6.8 hypothesizes **stabilization capacity `Σ = λ(π_random) − λ(π_strong) > 0`** — that
skilled play *suppresses* the amplification of small differences, with `Σ < 0` treated as the
rare, memorable case.

These are different measurements and are not formally in contradiction. But the direction is
opposed, on the same framework, with the same class of agent ladder. **Either `Σ < 0` is more
common than §6.8 expects — in which case the "memorable result" is the default and the framing
needs inverting — or the two measurements diverge, which is itself a result.** Worth a pilot on
two games before committing to §6.8's framing.

### 4.5 Paper B's construction found no occupant

No retrieved work applies a Lyapunov or finite-size Lyapunov exponent to board/tabletop game
trajectories, and none defines a prediction horizon in turns as a designer metric. **This is a
weak negative** — two queries on a narrow surface, and §7 of this file explains why absence
here is worth little.

---

## 5. Surfaces not reached — REQUIRED

**This run is bounded and does not satisfy the protocol's stopping rule.** `SEARCH-PROTOCOL.md`
§5 requires term-list exhaustion. Sixteen queries were issued against a cross-product of roughly
22 × 19 pairs plus 16 flat terms. **The vast majority of the term cross-product was not run.**

| Surface | Status | What would reach it |
|---|---|---|
| **Term cross-product** | ~16 slices of ~400+ run | A full `/litsweep` pass, or `.claude/workflows/litsweep.js` with `maxSlices` raised |
| **Jerdee & Newman full text** | Science Advances **403** | arXiv:2312.04711 PDF — exists, not read |
| **Goodman 2024, *Measuring Randomness in Tabletop Games*** | PDF would not extract | Direct download; it is the companion to the ToG paper and may contain the length analysis the ToG paper lacks |
| **Ben-Naim JQAS original** | PDF would not extract; read via the authors' HTML companion | The JQAS PDF, or arXiv physics/0512143 |
| **Duersch et al. original** | PDF would not extract | European Economic Review published version |
| **Forward-citation graph** | **Not traversed.** One citing work surfaced incidentally | Google Scholar "cited by" on retrievals 1, 2, 5. `SEARCH-PROTOCOL.md` §3 makes this **mandatory** — this run does not satisfy it |
| **dblp systematic enumeration** | Not run | dblp author pages for Goodman, Lucas, Perez-Liebana, Togelius, Browne |
| **CoG / CIG proceedings 2019–2025** | **Not hand-swept** | The analogue of `canvascurse`'s O-7. No such open item exists for this project yet |
| **IEEE Xplore** | No access | Institutional access |
| **Retrievals 3, 4, 5, 6, 7, 8, 9, 11, 12, 13** | `[T]` — **not read in the original** | Reading them. None may carry a novelty claim at this tier |
| **Non-English sources** | Not covered | — |

---

## 6. Draft ledger rows

**Not written to `DECISIONS_LEDGER.md`.** Drafted here for review — `PROTOCOL.md` §5.7: choices
are logged, not adopted, and the mark column is his.

| # | Decision | Where | If it changes | Mark |
|---|---|---|---|---|
| G-12 | **How Paper A positions against Goodman, Perez-Liebana & Lucas (ToG 2025)** — the same framework, the same agent ladder, the same community, asking a neighbouring question. Three options: (a) explicit delta in related work, injected-dial vs seed-control; (b) adopt seed-control as a second instrument and report both; (c) change testbed away from TAG to avoid the adjacency. | §8.2, §5.1; would land in related work | The related-work section, the novelty sentence, and possibly ledger **G-7** (TAG as testbed). *Raised by evidence 2026-08-17, not chosen.* | ☐ |
| G-13 | **Whether the noise operator is presented as novel at all**, given sticky actions (Machado et al., JAIR 2018) is an established one-parameter game-agnostic action-noise dial. | §2.1, §2.2, §8.3 contribution (1) | Contribution 1 of Paper A. §2.2's rejected-alternatives list currently omits sticky actions entirely. *Raised by evidence 2026-08-17.* | ☐ |
| G-14 | **Whether Δ_model is claimed as new**, given determinization / strategy-fusion work (Long, Sturtevant, Buro & Furtak 2010) already studies agents searching a model that does not match the true game. | §5.4, §8.3 contribution | §5.4 calls it *"possibly the most citable thing in the paper."* §8.2 cites no determinization work. *Raised by evidence 2026-08-17.* | ☐ |
| G-15 | **Whether §6.8's `Σ > 0` hypothesis survives**, given Goodman et al. find more skilled agents exploit randomness *more*. | §6.8 | Paper B's framing of stabilization capacity, and which result is presented as the surprise. *Raised by evidence 2026-08-17.* | ☐ |

---

## 7. What this run cannot tell you

`SEARCH-PROTOCOL.md` §7. It finds published work. It does not find what a CoG reviewer will
accept, whether the question is worth asking, or licence and reproducibility constraints.

And specifically here: **a `k = 0` on the specific conjunction, from a run that covered ~4% of
its own term cross-product and traversed no forward citations, is close to uninformative on its
own.** What this run actually established is §4.2 and §4.3 — that the framing, the operator and
one headline metric each have a named incumbent the document did not know about. That is the
result. The novelty finding is provisional.

---

_Written once, 2026-08-17. Not to be edited. A second run is a second file._
