# LITSEARCH — chaos-games — 2026-08-24

**Run type: FORWARD-CITATION SWEEP.** This is the mandatory forward pass that
`LITSEARCH-2026-08-17.md` §5 recorded as **not run**, and that `SEARCH-PROTOCOL.md` §3 makes
non-optional. It is **not** a second full sweep — the term cross-product is untouched and
remains ~4% covered from K1.

**Claim under test** (unchanged from K1, so the two runs compose): the execution-noise level at
which a game stops distinguishing strong from weak players is predictable from the game's
structure, with `1 − τ_skill ∝ L^(−1/2)` in decisions per player per match.

**Upper cutoff:** 2026-08-24.
**Forward-sweep targets:** K1 retrievals **1** (Goodman ToG 2025), **2** (Ben-Naim JQAS),
**5** (Jaffe AIIDE 2012), plus **Goodman CoG 2024 companion** (added — it is the nearer
incumbent artifact and K1 could not extract it).
**Run by:** Claude, in-session, no subagents.

> **NOT RED-TEAMED.** `PROTOCOL.md` §3.3 trigger **3** fires (states facts about the
> literature). Every tier below travels with its claim. The one `[V]` retrieval was read in
> the original; everything marked `[T]` **may not carry a novelty claim.**

---

## 1. Result

> **Specific conjunction — `k = 0` still, over the surface reached.** No forward citation of
> any of the four targets injects a controlled execution-noise dial, locates the threshold at
> which a skill ladder stops separating, **and** predicts that threshold from match length
> with a derived exponent.
>
> **Broad question — `k = 12 → 16`.** Four new works ask some version of *"how much of a
> game's outcome is skill versus chance."* Tier: one `[V]`, one `[V-sub]`, two `[T]`.

**R-16's specific question — has anyone taken up Goodman et al.'s printed §VI invitation? —
answers NO over the surface reached.** Their two 2024/2025 papers have **six** forward
citations between them; none pursues the skill-mitigates-stochasticity question.

**But the sweep found something larger than what it was sent to find.**

### 1.1 The headline finding: the incumbent is a research programme, not two papers

`tabletopgames.ai/Research.html` lists **a PhD thesis and at least six relevant papers** from
the same group. No register in this repo holds more than two of them.

| Work | Bears on |
|---|---|
| **Goodman, Perez-Liebana & Lucas, "Skill Depth in Tabletop Board Games", CoG 2024** | §1.2 the agent ladder · §4 `τ_rank` · §5.6 limitation 2 · ledger **G-3** |
| Goodman, Perez-Liebana & Lucas, "Measuring Randomness in Tabletop Games", CoG 2024 | already held — `READING-2026-08-22.md` |
| Goodman, Perez-Liebana & Lucas, "Seeding for Success", ToG 2025 | already held — **R-12** |
| **Goodman, J., PhD thesis 2025 — *"Dice, Cards, Action!"*, incorporating the above** | everything, and possibly **R-17**'s unpublished error-bound correction |
| **Ravichandran, Goodman & Lucas, "Evaluation of Perfect-Information Monte Carlo Tree Search in Imperfect-Information Games", CoG 2026** | **`Δ_model`** · **R-14**, which was narrowed on 2026-08-22 |
| **Goodman, Perez-Liebana & Lucas, "Following the Leader in Multiplayer Tabletop Games", FDG 2023** | **§3.4's feedback coefficient `θ`** — snowballing / leader dynamics |
| Goodman et al., "Fingerprinting Tabletop Games", CoG 2021; "Visualising Multiplayer Game Spaces", ToG 2021 | §5.1 game selection · ledger **G-6** |

**Only the third of these was in any register.** The publication list is a `[T]` source: it
establishes that these papers exist and roughly what they concern, **nothing more.**

### 1.2 Nearest work is now split, and one half moved

**(a) For the ladder and the skill-separation ceiling — NEW, and nearer than anything K1
found:** Goodman, Perez-Liebana & Lucas, **"Skill Depth in Tabletop Board Games", IEEE CoG
2024.** Read in the original (§V, §VII, §VIII). 16 TAG games, MCTS budget-doubling ladder, and
a **fitted three-parameter win-rate model** `S_adj = f(M, r, β; log₂(B/b))`:

- **`M`** — *"the maximum win rate a good player can achieve against a less skilled opponent"*,
  approached asymptotically as budget ratio → ∞, and **explicitly attributed to the game's
  stochasticity**: *"Games in which stochasticity is important, such as the deal of cards in
  Hearts or Poker are expected to have low M."*
- **`β`** — skill depth. **`r`** — rate of approach to `M`.
- Validated against BGG complexity ratings as a human proxy.

*Differs in:* their independent variable is **budget ratio at the game's native randomness**;
ours is an **injected noise parameter `p` at fixed budget ratio**. `M` is an asymptote in
skill; `τ_skill` is a threshold in noise. **They make no length prediction and derive no
exponent.** Their closest sentence — *"a better player can only be detected over a large
number of games so that the stochastic effects balance out"* — is about **repetitions of the
match**, not **decisions within a match**. That is exactly the distinction Paper A's `L`
depends on, and **it survives.**

**(b) For the scaling law:** unchanged — Ben-Naim, Vazquez & Redner (JQAS 2006). Its forward
set is 35 works, all sports statistics; nothing moved.

---

## 2. Exact queries issued

**Citation-graph API calls** (Semantic Scholar Graph API v1; OpenAlex attempted and refused —
see §5):

```
GET /graph/v1/paper/arXiv:2503.02686/citations?fields=title,year,venue,externalIds,abstract&limit=100
GET /graph/v1/paper/search?query=Measuring%20Randomness%20in%20Tabletop%20Games&...&limit=5
GET /graph/v1/paper/2209648958d3e3825897ad6a39b403c2707e20e7/citations?...&limit=100
GET /graph/v1/paper/search/match?query=Evaluating%20Competitive%20Game%20Balance%20with%20Restricted%20Play&...
GET /graph/v1/paper/c92a72f3a3c569c5925034d18ec6e53f6cf83a01/citations?...&limit=100
GET /graph/v1/paper/search/match?query=Parity%20and%20Predictability%20of%20Competitions&...
GET /graph/v1/paper/2f73f4dc5905b97d3a8a5e05f2be8704d36e4201/citations?...&limit=100
GET /graph/v1/paper/arXiv:physics/0512143?fields=title,year,citationCount,externalIds
GET https://dblp.org/search/publ/api?q=Evaluating+Competitive+Game+Balance+with+Restricted+Play&format=json&h=5
GET https://api.openalex.org/works?search=Seeding+for+Success+Skill+and+Stochasticity+Tabletop+Games   [refused — budget]
```

**WebSearch queries**, verbatim:

1. `"Seeding for Success" Goodman skill stochasticity tabletop games cited by`
2. `arXiv 2503.02686 Seeding for Success citations semantic scholar`
3. `"Quantifying Skill" "Opinion Trading" platforms luck chance paper`
4. `"Identifying Strategies in Dominion Using Playtrace Clustering" abstract IEEE Transactions on Games Owen`
5. `Soemers GameTable Working Group 1 London Meeting ICGA Journal 2025 abstract artificial intelligence cultural heritage`
6. `2026 tabletop games skill randomness threshold agent budget ladder noise injection win rate collapse CoG`
7. `"does greater skill" mitigate stochasticity games randomness effect beginner skilled players follow-up study 2026`
8. `"A Monte Carlo Approach to Skill-Based Automated Playtesting" AIIDE 2018 MCTS budget skill levels abstract`
9. `Symmetry 2026 "Connect-4" AI comprehensive taxonomy critical review methods metrics abstract MDPI`

**Full-text fetches:**

| Target | Result |
|---|---|
| `tabletopgames.ai/assets/pdf/Goodman2024SkillAnalysis.pdf` | **OK** — `curl -L` + `pdftotext`, 1347 lines. The `READING-2026-08-22.md` §1 route works again |
| `arxiv.org/html/2511.11611v1` | **OK** — upgrades K1 retrieval 11 from `[T]` |
| `tabletopgames.ai/Research.html` | **OK** — the publication list |
| `doi.org/10.1109/TG.2024.3520862` | 302 → IEEE Xplore, not followed |
| `mdpi.com/2073-8994/18/2/293` | **403** |

**Surfaced query 6 by accident, and it was the most valuable result of the run** — the Skill
Depth paper was not reachable from any of the four forward sets. See §5.

---

## 3. Retrievals

### 3.1 Forward set — Goodman ToG 2025 (K1 retrieval 1): **2 citing works**

| # | Work | Tier | Counts | Why |
|---|---|---|---|---|
| F1 | Soemers, Kowalski, Crist, Courts, Penn & Piette, *Bridging AI and Cultural Heritage: Outcomes From the GameTable WG1 London Meeting*, ICGA Journal, 2025 | `[T]` | **no** | Meeting report. Asks no research question |
| F2 | Banerjee et al., arXiv:2410.14363 | `[V-sub]` | — | **Already K1 retrieval 10.** No new count |

### 3.2 Forward set — Goodman CoG 2024 companion: **4 citing works**

| # | Work | Tier | Counts | Why |
|---|---|---|---|---|
| F3 | *Connect-4 AI: A Comprehensive Taxonomy and Critical Review of Methods and Metrics*, Symmetry 18(2):293, 2026 | `[T]` | **no** | Systematic review of Connect-4 AI; 49 studies. Not a skill/chance measurement |
| F4 | Owen, *Identifying Strategies in Dominion Using Playtrace Clustering*, IEEE ToG 17(3):631–641, 2025 | `[V-sub]` | **no** | Playtrace clustering for strategy discovery. **Uses a restricted-play framework** — Jaffe lineage — but asks nothing about noise, thresholds or length |
| F5 | Goodman et al., ToG 2025 | — | — | **Already K1 retrieval 1** |
| F6 | Bagchi, *Quantifying Skill on Opinion Trading Platforms*, tech report, March 2025 (IIT Delhi) | `[T]` | **yes — broad only** | Skill-vs-chance predominance on the Probo platform; persistence of performance across months. **Setting mismatch does not reduce k** (§5 adjudication). No injection, no ladder, no length |

### 3.3 Forward set — Jaffe AIIDE 2012 (K1 retrieval 5): **95 citing works**

Filtered on `noise|stochast|random|luck|chance|skill|threshold|collaps|length|depth|balance|perturb|MCTS|budget`; 20 hits, all in the **game-balance** lineage. None counts toward the specific conjunction.

| # | Work | Tier | Counts | Why |
|---|---|---|---|---|
| F7 | Horn, Miller, Smith & Cooper, *A Monte Carlo Approach to Skill-Based Automated Playtesting*, AIIDE 2018 | `[T]` | **no** | Stratabots — agents parameterised by **skill sets** — for Foldit progression analysis. **A supporting citation for agent-as-skill-proxy** that §8.2 does not list. Not a noise or threshold measurement |
| F8 | *Assessing Game Balance with AlphaZero: Exploring Alternative Rule Sets in Chess*, arXiv 2020 | `[T]` | **no** | Rule-set variation, not noise injection |
| — | 18 further balance papers (Pokémon VGC balance track CoG 2025; Baldur's Gate 3 progression balancing CHI 2025; meta-discovery ToG 2024; Ludus AAAI 2022; …) | `[T]` | **no** | Character/rule balance. None defines a skill-collapse threshold |

### 3.4 Forward set — Ben-Naim JQAS (K1 retrieval 2): **35 citing works**

| # | Work | Tier | Counts | Why |
|---|---|---|---|---|
| F9 | Ben-Naim & Hengartner, *Randomness in Competitions*, J. Statistical Physics, 2012 | `[T]` | **yes — broad** | Same lineage, same authors; upset probability over a season. Games-per-season, not decisions-per-match |
| F10 | *Luck is Hard to Beat: The Difficulty of Sports Prediction*, KDD 2017 | `[T]` | **yes — broad** | Luck as a limit on predictability, sports. No injection, no agents |
| — | 33 further works | `[T]` | **no** | Sports competitive-balance statistics — football leagues, US major sports, forecast optimality |

### 3.5 Retrieved outside the forward sets

| # | Work | Tier | Counts | Why |
|---|---|---|---|---|
| **F11** | **Goodman, Perez-Liebana & Lucas, *Skill Depth in Tabletop Board Games*, IEEE CoG 2024** | **`[V]`** (§I, §V, §VII–VIII read in the original) | **yes — and it is the new nearest work for the ladder half** | See §1.2(a) and §4.1 |
| F12 | Goodman, J., *Dice, Cards, Action! The Analysis, Play and Design of Multiplayer Tabletop Board Games with MCTS*, PhD thesis, QMUL, 2025 | `[T]` | **deferred** | Title and existence only. **Highest-value unread item in the project** — see §4.4 |
| F13 | Ravichandran, Goodman & Lucas, *Evaluation of Perfect-Information Monte Carlo Tree Search in Imperfect-Information Games*, IEEE CoG **2026** | `[T]` | **deferred** | Title and existence only. Lands on `Δ_model` and **R-14** |
| F14 | Goodman, Perez-Liebana & Lucas, *Following the Leader in Multiplayer Tabletop Games*, FDG 2023 | `[T]` | **deferred** | Title and existence only. Lands on §3.4's `θ` |
| F15 | *Quantifying Skill and Chance: A Unified Framework for the Geometry of Games*, arXiv:2511.11611 | **`[T]` → `[V-sub]`** | **yes (already counted in K1 as retrieval 11)** | **Tier upgraded.** Read via arXiv HTML. Skill–Luck Index `S(𝒢) ∈ [−1,1]` from game-tree decomposition. **Confirmed: no parameter sweep, no threshold, no length scaling.** Its `Σ` is per-turn outcome volatility — **note the symbol collision with theory §6.8's stabilization capacity `Σ`** |

---

## 4. Findings

### 4.1 The skill ladder is more occupied than any register recorded

R-12 recorded the *randomness* framing as occupied. **The *skill ladder* framing is occupied
too, at the same venue, in the same year, by the same group** — and the lineage behind it is
older than this project's registers show: **Lantz, Isaksen, Jaffe, Nealen & Togelius (AAAI-W
2017) → Browne, *Quickly Detecting Skill Trace in Games*, CoG 2022 → Goodman et al., CoG
2024.**

**K1 already retrieved Browne 2022** — retrieval 9, *"Quickly Detecting Skill Trace in Games",
title/abstract only* — **and did not connect it.** It is reference [4] of the Skill Depth
paper and the direct methodological parent. That is a `[T]`-tier retrieval whose significance
was invisible until the citing paper was read in the original, which is the case for
`SEARCH-PROTOCOL.md` §4 in one line.

Theory §8.2 cites Lantz et al. It cites neither Browne 2022 nor Goodman et al. 2024.

### 4.2 NEW RISK — the ladder's rungs are an artifact of MCTS parameter choice, and they published the demonstration

Verbatim, Skill Depth §VII-A:

> *"In these games, the default setting is in a poor region of MCTS parameter space and the
> high ST arises because this poor policy makes solid progress as computational budget is
> increased. **A small shift in MCTS parameter space gives a better policy that with a 32ms
> budget can easily defeat a Classic 1024ms agent.** The agents rapidly reach the plateau of
> perfect play, and the estimated ST correctly plummets."*

**A 32× budget advantage, reversed by a parameter change.** And they report that per-game
tuning *"makes a significant change in the rating of some games."*

Theory §1.2 instantiates the ladder as `B_j = B_0 · 2^j` and §1.2's stated safeguard is that
`W_0` be **monotone in `j`**. Monotone it will be — budget-monotonicity is not the property at
risk. What their result shows is that the ladder's **calibration is per-game and
parameter-dependent**: the same budget ratio buys different amounts of skill in different
games depending on where the default MCTS parameters sit for that game.

`SURFACES.md` states that **all four thresholds are measured against the ladder.** The headline
regression compares thresholds **across games**. A per-game, algorithm-induced miscalibration
of the ladder is therefore a confound in `β₁` that no register holds and that §5.2's three
predictors cannot absorb. **This is proposed as R-18.**

### 4.3 Independent corroboration of the small-n regression problem

Skill Depth §VII-A, on their own fits: *"there is random noise in y with the slope of the
regression line on just 7 points"*, and their rank correlations against BGG complexity reach
**p = 0.24 and p = 0.16** — null.

The incumbent, with 16 games, does not achieve a significant fit of a game-difficulty measure
against a human proxy. Theory §5.2 proposes `β₁` over **8–12 games with three predictors**.
This is external evidence for the power concern already open against §5.2, and it strengthens
the case for simulating that regression before September rather than after.

### 4.4 R-17's correction may already be readable

Goodman's 2025 PhD thesis *incorporates* the papers, and R-17's open item is an error-bound
correction the CoG 2024 paper described as *"current work in progress."* **A thesis is where
work-in-progress lands before it is published separately.** If the fixed-`p` binomial
correction is in that thesis, `BUDGET.md` §1's `M ≈ 785` can be resolved from a readable
source instead of waiting on a publication. This is the highest-value unread item in the
project and the `pdftotext` route is known to work on this group's PDFs.

### 4.5 R-14 needs re-opening, not merely narrowing

R-14 was narrowed on 2026-08-22 on the grounds that Long et al. (2010) formalise no mismatch
quantity and hold depth constant. That reasoning is unaffected. But **Ravichandran, Goodman &
Lucas have a CoG 2026 paper evaluating PIMC in imperfect-information games** — the incumbent,
at the target venue, in the current cycle, on the exact mechanism `Δ_model` measures. Whether
this collides with `Δ_model` or supports it **cannot be judged from a title**, and §5.4 calls
`Δ_model` *"possibly the most citable thing in the paper."*

### 4.6 What did not move

- **The specific conjunction is still unoccupied** over the surface reached. Injection,
  threshold, and a derived length exponent still do not co-occur in any retrieved work.
- **The `L` distinction holds.** Every length-adjacent statement retrieved in this run —
  Skill Depth's *"large number of games"*, Ben-Naim's season length, Duersch's critical
  repetition frequency — is about **repetitions of a match**. None is about **decisions within
  a match**. That distinction is Paper A's load-bearing one and it survived a second run.
- **R-16 answers NO so far.** Six forward citations across both Goodman 2024/2025 papers;
  none takes up the §VI question.

---

## 5. Surfaces not reached — REQUIRED

**This run does not satisfy `SEARCH-PROTOCOL.md` §5's stopping rule.** It is a forward sweep,
not a term-exhaustion run.

| Surface | Status | What would reach it |
|---|---|---|
| **Term cross-product** | **Still ~4% covered.** Untouched by this run | A full `/litsweep` pass |
| **Goodman PhD thesis 2025** | **Not read. Not located.** | QMUL research repository; `pdftotext` route. **§4.4 — highest value** |
| **Ravichandran, Goodman & Lucas, CoG 2026** | **Not read.** Title from a publication list only | `tabletopgames.ai` PDF or IEEE Xplore. **§4.5** |
| **Goodman et al., FDG 2023 (Following the Leader)** | **Not read.** Title only | FDG proceedings / `tabletopgames.ai`. Bears on §3.4's `θ` |
| **Browne, CoG 2022 (Skill Trace)** | **Still `[T]`** from K1. Now known to be the methodological parent | IEEE Xplore or author copy |
| **Tavener, "UCT Skill Ladders" (2020)** | Not retrieved. Reference [5] of Skill Depth; a web report | `mrraow.com/uploads/AiAiReports/uct_skill_ladders.html` |
| **Lantz et al. 2017 in the original** | Still `[T]` from K1 (retrieval 12) | AAAI Workshops 2017 |
| **Skill Depth §II, §III, §VI** | Read §I, §V, §VII, §VIII only — `[V]` covers those | The remaining sections of a file already on disk |
| **OpenAlex** | **Refused — daily budget exhausted** (`"Insufficient budget… Resets at midnight UTC"`) | Re-run after 00:00 UTC. A second, independent citation graph |
| **Semantic Scholar coverage** | Heavy 429 rate-limiting; `/search` largely unusable. **S2's graph lags for 2026 work**, and the Skill Depth paper was **not reachable from any forward set** | An S2 API key. **Note this is how a CoG 2024 paper by the incumbent stayed invisible to a citation-graph sweep** |
| **Ben-Naim record quality** | The matched S2 record is a **duplicate-looking entry** (`"Journal of Quantitative Analysis in Sports Parity and Predictability of Competitions"`, year 2010, no venue, 35 citations). The canonical record may carry more | Crossref DOI resolution, then a fresh citation pull |
| **Google Scholar forward graph** | **Not traversed** — no programmatic access | Manual `cited by` on the four targets |
| **IEEE Xplore** | No access | Institutional access |
| **F1, F3, F6–F10, F12–F14** | `[T]` — not read in the original | Reading them. **None may carry a novelty claim at this tier** |
| **CoG / CIG 2019–2025 hand sweep** | **Still not run.** K1 flagged it; no open item exists for this project | The analogue of `canvascurse`'s O-7 |
| **Non-English sources** | Not covered | — |

---

## 6. Draft ledger rows

**Not written to `DECISIONS_LEDGER.md`.** Drafted for review. `PROTOCOL.md` §5.7 — choices are
logged, not adopted, and the mark column is his. These are **G-19…G-21**, on top of the seven
already drafted and unwritten (G-12…G-18).

| # | Decision | Where | If it changes | Mark |
|---|---|---|---|---|
| **G-19** | **How Paper A positions against *Skill Depth* (CoG 2024)** — their `M` is a per-game skill-separation ceiling explicitly attributed to stochasticity, fitted parametrically over a budget ladder on 16 TAG games. Options: (a) state the delta in related work — asymptote-in-skill vs threshold-in-noise; (b) adopt `M`/`β`/`r` as covariates in §5.2, treating their model as measured input; (c) reframe `τ_skill` explicitly as the noise-axis complement of their skill-axis `M`, and cite the pair as a two-axis characterisation. | §8.2, §5.2, §4; contribution (2) and (4) | The related-work section, possibly §5.2's predictor set, and whether `τ_rank` is claimed as new at all. *Raised by evidence 2026-08-24, not chosen.* | ☐ |
| **G-20** | **Whether the skill ladder is tuned per game or held at fixed MCTS parameters.** The incumbent has published that per-game tuning changes ratings significantly, and that a parameter shift let a 32 ms agent beat a 1024 ms agent. Options: (a) fixed parameters, and declare the resulting ladder miscalibration as a limitation; (b) tune per game as they do, accepting that "budget" then no longer means one thing across games; (c) report both and treat the difference as a measurement. | §1.2, §5.6; ledger **G-3** | All four thresholds and the headline regression's cross-game comparability. **Also a budget change** — (b) and (c) multiply the run count. *Raised by evidence 2026-08-24.* | ☐ |
| **G-21** | **Whether `Σ` is renamed.** Theory §6.8 uses `Σ` for stabilization capacity; arXiv:2511.11611 uses `Σ` for per-turn outcome volatility in the same subfield. | §6.8 | Notation only, but in a paper that will sit beside that one. Cheap now, awkward later. *Raised by evidence 2026-08-24.* | ☐ |

---

## 7. Proposed risk-register changes

Not applied. `RISKS.md` is a live register and these are proposals.

| ID | Change |
|---|---|
| **R-18** | **NEW — ACTIVE.** *The skill ladder's calibration is an artifact of MCTS parameter choice, per the incumbent's own published experiment.* Trigger: any cross-game threshold comparison. If it fires: `β₁` carries a per-game confound; mitigation is G-20, and every option there is a budget change |
| **R-14** | **Re-open from NARROWED to ACTIVE.** Ravichandran, Goodman & Lucas, CoG **2026**, on PIMC in imperfect-information games. The 2010-based narrowing reasoning is untouched; a 2026 incumbent paper is a new exposure |
| **R-12 / R-16** | **Widen.** The exposure is a **research programme with a PhD thesis**, not two papers. Both rows currently name two artifacts |
| **R-17** | **Add a route.** Goodman's 2025 thesis may contain the error-bound correction. Reading it may resolve `M ≈ 785` without waiting on publication |
| **R-1** | **Unchanged — still PARTLY DISCHARGED.** The forward pass is now run for four targets, which was §5's largest gap. The term cross-product is not, so R-1 does not retire |

---

## 8. What this run cannot tell you

`SEARCH-PROTOCOL.md` §7, plus one specific to this run:

**The most valuable retrieval of this sweep was not reachable by the sweep's own method.**
*Skill Depth* is a CoG 2024 paper by the incumbent, on this project's central instrument, and
it appears in **none** of the four forward-citation sets. It surfaced from a keyword query
issued as an afterthought. A citation graph finds what cites your targets; it does not find
what sits **beside** them. `FAILURE-MODES.md` F-10 in its general form — and the argument for
the CoG/CIG hand sweep that §5 has now flagged twice.

---

_Written once, 2026-08-24. Not to be edited. Not red-teamed. A second run is a second file._
