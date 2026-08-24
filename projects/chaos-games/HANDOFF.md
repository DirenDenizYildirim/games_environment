# HANDOFF — chaos-games
_Last session: 2026-08-24 (second) | main | d170627 | JVM toolchain installed; build not yet started_

## Current state

Theory document 578 lines, v0.1. **No code yet.** Preregistration is a stub, not locked.

**The literature phase is closed** — deliberately, by his call. Two sweeps ran; the specific
conjunction (inject a dial → locate the skill-collapse threshold → predict it from length with
a derived exponent) returned **`k = 0` both times**, and the `L` distinction — decisions
*within* a match, not repetitions *of* one — survived every length-adjacent paper retrieved.
That is the result. **No further sweeping.** What remains unrun (term-exhaustion at ~4%, the
CoG/CIG hand sweep) blocks a novelty sentence, which is a March deliverable, not a September one.

**§7.1 is wrong in two compounding ways** (`DERIVATION-2026-08-24.md`). Correcting both
**restores** the `L^(−1/2)` law — §7.1 as written implies the central claim fails in any game
with appreciable λ — while weakening the A↔B bridge from *exponential in λL* to *saturating*.

**Register cleaned before code:** 18 live rows → **15**. R-12/R-13/R-14 retired into binding
writing obligations; R-15's provenance corrected; R-16 → WATCHING; R-1 restated.

## In flight

**Nothing half-built.** All four archives are write-once and closed. Working tree clean.

Two reads stopped mid-Block-A, **both external, neither a dead end**:

1. **Goodman 2025 PhD thesis** — the `tabletopgames.ai` link is stale (QMRO moved to DSpace 7),
   and **QMRO is network-blocked from this machine** (`"Web Page Blocked!"` / `000` / `socket
   hang up`); CORE is Cloudflared. **Handle `123456789/108265`.** Needs a browser. It is a
   **budget errand, not a novelty errand** — it may hold R-17's error-bound correction.
2. **OpenAlex** — refused at 16:14 UTC, *"Insufficient budget… Resets at midnight UTC."* Will
   have reset by the next session.

## Blocked

Nothing blocks code. `R-17` still blocks quoting `M ≈ 785` or the ~10⁶ figure.

## Next actions — the first build session

Ordered. **Tiers matter more than usual here: most of what you would naturally build first is
Tier 2.**

**Before the first line of code**

1. **Review `SURFACES.md`** — Tier 2 — done means: read against what is actually about to be
   built, and anything missing is added. Its own header says the gate should read a list written
   from a codebase, not from a document. **This is the declared first item of the first coding
   session.**

**Build immediately — no gate**

2. **Repo skeleton** — Tier 1 — package layout, test runner, CI, config plumbing. Explicitly
   *not* Tier 2 per `SURFACES.md`'s own exclusion table. Do not memo it.
3. **TAG running headless** — Tier 1 — done means: one game, one MCTS agent, one match, from a
   script, twice, identical output. A toolchain check. **The moment an adapter is written it
   becomes Tier 2.** **The JDK half is discharged** — see Standing; what remains is TAG itself.
4. **Measure `L` for every game TAG ships** — Tier 1 — done means: a table of
   decisions-per-player-per-match across the roster, with variance.
   **Highest-value thing available.** §5.1 says spread in `L` *"dominates every other
   criterion"* — an order of magnitude, ~10 to ~200. **R-2** says that rests on an unchecked
   fact about someone else's framework, and if the spread is not there the headline regression
   has no leverage and the project changes shape. Also discharges **O-12**. The 16 games in
   `READING-2026-08-24.md` §1.6 are a starting roster; **BGG complexity is not `L`.**

**Needs a build memo → stop → approval. In this order.**

5. **The RNG / seeding path** — Tier 2 — counter-based hash keyed by
   `(root_seed, condition_id, match_id)`; determinism test bit-identical across core counts and
   batch sizes. **First** because Paper A needs it too (§5.3's colour-swapped pairs need
   identical seeds), §6.4 warns it takes longer than expected inside an existing framework, and
   its absence is a **silent** invalidator.
6. **The run artifact schema** — Tier 2 — mode (`explore`/`confirm`), seed, commit, prereg hash,
   per-condition search budget. Mode recoverable from filename, manifest **and** plot watermark.
7. **The noise operator** — Tier 2 — blocked on **G-2**.
8. **The skill ladder** — Tier 2 — blocked on **G-20**.
9. **§5.5's sanity checks** — Tier 1 once 7 and 8 exist — pure-luck control `W_p ≡ ½`;
   `W_1 = ½` every game and rung pair; `G_0` ladder monotone; `W_p` non-increasing. §5.5 says
   run these *first*, before burning budget. A `G_1` failure is almost always asymmetric seeding
   — which is why 5 comes before this.

**Desk items that survive, none blocking**

10. Get the thesis onto disk (R-17). 11. Re-run OpenAlex. 12. **Append the ledger rows.**
13. **Red-team the four unreviewed artifacts.** 14. O-9 — Palmer, Kantz.

## Open questions

His. **Ten rows drafted and unwritten; `DECISIONS_LEDGER.md` §3 still ends at G-11.**

- **G-2** — uniform action replacement as the noise operator, vs perturbation toward *plausible*
  actions. **Blocks build item 7.** §9 Q1's cheap mitigation: run both on one game early.
- **G-20** — ladder tuned per game, or fixed MCTS parameters. **Blocks build item 8, and it is a
  budget change either way** — their tuning uses NTBEA, which `BUDGET.md` does not cost.
- **G-3, G-8, G-11** — unchanged. **G-12…G-19, G-21** — drafted, unwritten.
- **G-22 — NEW, drafted here, not written.** *Whether the project accepts `k = 0` over a
  deliberately bounded surface (~4% of the term cross-product, no hand sweep) as the basis for
  its novelty position.* Where: any novelty sentence, §8.3. If it changes: the search reopens
  before March. **Raised 2026-08-24 by his decision to close the search phase — logged, not
  adopted.**

## Traps for next session

**Build**

- **§5.3's ML fit will destabilise exactly where the threshold lives.** The incumbent needed
  **L2 regularisation** on the same class of parametric win-rate fit because *"high noise in
  low-skill games could cause overfitting"* — and this project drives games into that regime on
  purpose. Belongs in item 7's memo.
- **Their `M` is not identifiable in several games** — budget is unbounded, so the asymptote
  escapes the data. **`p ∈ [0,1]` is bounded and `G_1` is a defined endpoint**, so a `p`-sweep
  covers its whole domain. That is the strongest `[V]`-backed argument that the injected-noise
  instrument is *better conditioned*, not merely different. **G-19 material — do not lose it.**
- **Their default agent is Open Loop IS-MCTS with root redeterminisation**, not vanilla MCTS.
  §1.2 under-specifies the agent for imperfect-information games.
- **`Hearts` is a named `Σ < 0` candidate** — the incumbent's own unexplained counterexample, in
  print. Make it one of §6.8's two pilot games.

**Theory**

- **§7.1 has two defects, not one.** The missing `1/L` is the easy one to miss: it substitutes a
  **total over injection times** into §3.2's **per-decision** variance slot, and fails the
  `λ → 0` limit check that §3.4 performs on itself and passes. **`t_sat` is `T_pred`** — §6.7
  already names the quantity §7 needs.
- **Do not repeat that boundedness breaks the `L^(−1/2)` law.** Said that way mid-session; wrong.
  Fixing **both** defects restores it.
- **§3.4's `θ` is unoccupied by anything retrieved.** *Following the Leader* (FDG 2023) does
  **not** bear on it — that was a title-only guess, corrected in `READING-2026-08-24.md` §3.

**Record**

- **R-15 read `"Verified verbatim"` on a `[T]` source for two days.** The quote turned out real
  — **by luck, not process.** This is the one place F-1 reached the live register. If a row says
  *Verified*, check the tier of the underlying read.
- **`LITSEARCH-2026-08-24.md` §1.1 still contains one unverified guess** — *Fingerprinting* /
  *Visualising* → "§5.1 · G-6". Banner-marked at the top of that file. **Do not act on it.**
- **A `[T]` marker does not stop a bold declarative table cell being read as a finding.** Tier
  the cell, not the footnote.
- **Both 2026-08-24 archives carry appended correction banners.** No original text was altered.
- **Four artifacts are NOT red-teamed**: both `READING`s, `LITSEARCH-2026-08-24`, `DERIVATION`.

**Standing**

- **The JVM toolchain is installed** (2026-08-24): `jdk21-openjdk 21.0.11.u10-1` and
  `maven 3.9.16-1`, via `pacman -U` from `archive.archlinux.org` — **not** from the live
  mirrors. This machine's package database is from **2026-07-11** and current mirrors 404 on
  that JDK version; the archive route pins the versions the stale database expects, which is
  why it needed no system upgrade and no reboot. `mvn -v` reports Java 21 at
  `/usr/lib/jvm/java-21-openjdk` and finds it unaided — **`JAVA_HOME` is not set and does not
  need to be.** **A `pacman -Syu` will replace all four packages**: re-run `mvn -v` after any
  system upgrade before blaming a build failure on TAG.
- **The build network is open from this machine, unlike the literature network.**
  `repo.maven.apache.org`, `github.com` and `plugins.gradle.org` all return 200.
  **QMRO and CORE remain blocked** — the two facts are unrelated; do not generalise from
  either to the other.
- `tabletopgames.ai/Research.html` indexes this group's PDFs; `curl -L` + `pdftotext` works.
  **QMRO and CORE are blocked from this machine — do not retry.**
- **`Σ` collides** — theory §6.8 vs arXiv:2511.11611. Ledger **G-21**.
- **TAG is JVM** (G-7). **Paper B before Paper A** is the sequencing trap. This document has no
  seed in `topics.md` (X-1b).
