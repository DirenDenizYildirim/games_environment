# DIARY — chaos-games

_Surprises, dead ends, changed beliefs. Append-only._
_Format: `../../docs/PROTOCOL.md` §5.2._

## 2026-08-22

**Did:** Extracted and read the Goodman CoG 2024 companion that K1 recorded as unextractable,
plus Long et al. (AAAI 2010) in full. `READING-2026-08-22.md`.

**Surprised by:** two things, in opposite directions.

**The companion does contain the length analysis** — Figure 2, rounds-to-win in Love Letter
swept 1 → 50, Trimmed Span 1.0 → 0.64. The claim survives, because it is one game varying a
rule parameter, measuring outcome *spread* rather than a collapse *threshold*, with no
functional form fitted. But the qualitative relation is now theirs, at our venue, on our
framework, and no sentence can present it as ours.

**Their §VI future work is our paper**: *"does greater skill increase or decrease the ability
to mitigate stochasticity... Are there games for which randomness has a large effect on
beginner players, but not for more skilled players?"* Written in 2024 by the group that owns
TAG. The 2025 ToG paper answers part of it. That is not a collision — it is a clock, and it
had been sitting unread in a PDF this project already knew about.

**Changed my mind about:** **R-14, in the direction of relief.** Long et al. was carried as
"the largest unpatched hole K1 found." They formalise no model-mismatch quantity at all, use
no skill ladder, inject no noise, and hold tree depth constant at 8. Their mismatch is
*informational*; Δ_model is *execution-noise*. Better: they establish that structural game
properties predict when an algorithmic mismatch causes loss, which is the *shape* of this
project's argument — so they are partly a supporting citation. §8.2 must cite them, but
Δ_model need not drop to a measurement. That is a third option G-14 never listed.

**Dead end:** the AAAI OJS download endpoint 404s and scispace 403s. Sturtevant hosts the
paper on his own faculty page, which is where it came from. Generally: `arxiv.org/html/…` and
ar5iv give the fetch layer's summariser usable prose but give me nothing quotable — only
fetching the PDF to disk and running `pdftotext` produces text I can read myself, and that is
the difference between `[T]` and `[V]`. K1's "the PDF would not extract" was a limitation of
the route, not of the file.

**Unresolved:** **G-11.** Their §VI says the fixed-`p` binomial understates the games needed
when seed variance is large, and that the correction is work in progress. M ≈ 785 and the
whole compute budget come from that model. We cannot adopt a correction that has not
published, cannot defend the current number against a reviewer who has read their §VI, and
cannot tell how far off it is. Nothing in `BUDGET.md` anticipated being wrong from the
outside.

## 2026-08-24

**Did:** ran the mandatory forward-citation sweep on K1 retrievals 1, 2, 5 plus the CoG 2024
companion (`LITSEARCH-2026-08-24.md`), and checked §7.1's variance integral against §6.2's own
boundedness statement (`DERIVATION-2026-08-24.md`). Both write-once, neither red-teamed.

**Surprised by:** **the forward sweep did not find the most important paper, and could not
have.** *Skill Depth in Tabletop Board Games* is a CoG 2024 paper by Goodman, Perez-Liebana &
Lucas — the incumbent, the target venue, the year we already knew about — on this project's
central instrument, the MCTS budget ladder. It appears in **none** of the four forward-citation
sets. It surfaced from a keyword query issued almost as an afterthought. A citation graph finds
what cites your targets; it does not find what sits *beside* them, and the two 2024 CoG papers
by the same authors do not cite each other in a way any graph I could reach exposed. The
protocol's forward sweep is mandatory and it was the right thing to run, but the run's own
best result is an argument for the hand sweep §5 has now flagged twice.

Second surprise, inside that paper: *"A small shift in MCTS parameter space gives a better
policy that with a 32ms budget can easily defeat a Classic 1024ms agent."* A 32× budget
advantage reversed by a parameter change. §1.2's safeguard is that `W_0` be monotone in `j`,
and it will be — that was never the property at risk. The property at risk is that the same
budget ratio buys different amounts of skill in different games, which makes every cross-game
threshold comparison carry a per-game confound. That is R-18, and every way out of it costs
compute.

Third: K1 had already retrieved Browne's *Quickly Detecting Skill Trace in Games* (CoG 2022) as
retrieval 9, at `[T]`, title and abstract only, and recorded it as a near-miss. It is reference
[4] of the Skill Depth paper and the direct methodological parent of the entire skill-ladder
line this project builds on. The retrieval was correct and its significance was invisible until
something citing it was read in the original. That is `SEARCH-PROTOCOL.md` §4's whole argument,
demonstrated on our own archive rather than on someone else's.

**Changed my mind about:** **the boundedness problem, twice, within one derivation.** I opened
§7.1 expecting to find that §6.2's bounded value space breaks the `L^(−1/2)` law — a second
saturation mechanism on top of §3.4's, firing even in the martingale regime. It looked clean
and it was wrong. §7.1 has *two* defects, not one: it also substitutes a total over injection
times into §3.2's per-decision variance slot, a missing factor of `L`. Fix only the boundedness
and the law does break. Fix **both** and `γ²_eff` saturates at a constant and the law is
**restored** — for every game, at every λ, which is better than the document's own position,
since §7.1 as written implies the central claim fails in any game with appreciable λ.

The tell was sitting in the document. §3.4 verifies its own `θ → 0` limit and says *"It does."*
§7.1 performs no such check and does not pass one. A section that checks its limits next to a
section that does not is where to look.

What actually weakens is the bridge — the thing §0 calls *"your strongest single result"*.
Exponential in `λL` becomes saturating in `λL`, ceiling `(Δ_max/d₀)²`, and §7.1's instruction to
add `λ̂` linearly to §5.2's regression tests a functional form the corrected derivation does not
predict. `t_sat`, the saturation time the corrected form needs, is `T_pred` from §6.7. The
document already has the quantity and does not use it two sections later.

**Dead end:** OpenAlex is not available as a second citation graph — it now meters by daily
budget and refused mid-run (`"Insufficient budget… Resets at midnight UTC"`). Semantic Scholar's
`/search` endpoint is unusable under sustained 429s; `/paper/{id}` and `/paper/search/match`
survive with `curl --retry --retry-delay`. MDPI 403s, IEEE Xplore is closed. The `pdftotext`
route from 2026-08-22 works again and works on `tabletopgames.ai/assets/pdf/` generally — that
is now two for two and should stop being rediscovered.

**Unresolved:** **whether ten unwritten ledger rows is still a queue or has become a backlog.**
Three more were drafted today; §3 of `DECISIONS_LEDGER.md` still ends at G-11, where it ended
on 2026-08-17. `/session-end` step 6 says to append them; the practice recorded in this
project's own handoff says wait for his go-ahead on a portfolio-wide file. Both readings are
defensible and they have been diverging for a week. Two of today's three — G-19 and G-20 — bear
on §5.2's predictor set and on the compute budget, which are exactly the things that want
deciding *before* September rather than after.

**Addendum, same day — Block A.** Three reads (`READING-2026-08-24.md`). R-18 went from
proposed to confirmed on one sentence of §VI — *"for others this varied"* — which is the
difference between a limitation and a confound, and it widened from one axis to three.

The thing worth recording is smaller and about process. I wrote in
`LITSEARCH-2026-08-24.md` §1.1 that *Following the Leader* (FDG 2023) "lands on §3.4's `θ`".
That entry was tiered `[T]` — a title from a publication list — and tiering it honestly is the
only reason the error was cheap. It is about **agent objective functions**, not game feedback
structure, and `θ` remains unoccupied. Roughly four hours between writing the guess and
reading the paper. The `[T]` marker did its whole job: the claim was already fenced when it
turned out to be wrong, the archive is write-once so the wrong sentence stays visible, and the
correction is a second file rather than a silent edit. That is the mechanism working as
designed, and it is the first time in this project it has caught one of **mine** rather than
one inherited from a source.

**Second addendum, same day — the search phase closed, and a near-miss.**

**Changed my mind about:** how much narrowing is worth doing before code. He stopped the
literature work, and the diagnosis was right and checkable in the artifacts: the declared sweep
was four forward sets, I finished those and then chased the thesis, the PIMC paper and the FDG
paper — none of them in the protocol — because each read produced its own next target. That is
a loop, not a method. `SEARCH-PROTOCOL.md` §1 says `k` is *"reported as a number, not a verdict
— nothing in this repo passes or fails on its output"*, and §5's stopping rule is
term-exhaustion, not "keep pulling threads." Meanwhile the actual result — **`k = 0` on the
specific conjunction, twice, and the `L` distinction surviving both runs** — got one line and
the adjacency inventory got three hundred. `FAILURE-MODES.md` F-6 is the parent project dying
on a gate that was *"trivially satisfiable as an objection and unfalsifiable as a defence"*;
over-narrowing is that failure in a different costume. The novelty sentence is a March
deliverable and there is no novelty claim in flight, so pinning it against a moving premise was
work done twice.

**Surprised by:** R-15 was carried as *"Verified verbatim"* for two days on a source
`READING-2026-08-22.md` §3 simultaneously marked `[T]` — *"fetch-layer summary only."* Reading
the original settled it: the sentence is genuine, line 854, word for word. **It was right by
luck, not by process.** The interesting part is what only the original showed — their Figure 3
uses **homogeneous agents**, so the opposition to §6.8's cross-policy `Σ` is weaker than the
row asserted, and they name **Hearts** as a counterexample to their own trend that they cannot
explain. §6.8 says one such game would be worth foregrounding. The register had been holding an
opportunity filed as a threat, which is the same bias as the paragraph above, pointed inward.

**Unresolved:** the ledger, still. Ten drafted rows and §3 ends at G-11 where it ended on
2026-08-17. **G-2 and G-20 now block specific build items**, so this stopped being a filing
question and became a scheduling one.
