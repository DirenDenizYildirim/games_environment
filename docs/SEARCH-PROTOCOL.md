# SEARCH PROTOCOL — declared pre-emption search (games)

Fixed in advance. Run once per novelty claim. Archived. **Reported as a number, not a
verdict** — nothing in this repo passes or fails on its output.

The protocol exists because the alternative failed. The parent project tried the gate *"the
violation must be unexamined in the source literature"* — a universal negative over an
undefined corpus, with no search protocol, no venue list, no stopping rule and no adjudicator.
It was trivially satisfiable as an objection and unfalsifiable as a defence (`FAILURE-MODES.md`
F-6). This replaces it with something that can actually be run and audited.

The `/litsweep` skill and `.claude/workflows/litsweep.js` implement it.

---

## 1. The reported field

For the claim under test, report, **adjacent to the claim itself**:

> This question has been asked in **k** retrieved works; the nearest is **X**; our claim
> differs in **Y**.

`k = 0` is a legitimate and **weak** result — a negative over a bounded surface, to be read
against §6. It is not evidence of novelty; it is the absence of evidence against it,
quantified and auditable.

Print it the way the comparison type is printed. It is a field, not a gate.

---

## 2. Terms — fixed, enumerated, exhausted

Three groups. **Every term in A is crossed with every term in B; C is run flat.** The run is
finished when the cross-product is exhausted, **not** when a satisfying answer appears.

**A — the phenomenon.**
skill expression · skill ceiling · skill differentiation · execution noise · action noise ·
input noise · motor noise · misclick · stochasticity · randomness · determinism · outcome
variance · luck · chance · divergence · sensitivity to initial conditions · perturbation ·
predictability horizon · difficulty · indirect control · actuation budget · resource budget

**B — the setting.**
game · video game · digital game · board game · card game · platformer · playtesting · level
design · procedural content generation · game balance · difficulty curve · dynamic difficulty
adjustment · game AI · Monte Carlo tree search · general game playing · self-play ·
matchmaking · esports · player modelling

**C — the result shape** (run flat, not crossed).
skill/luck ratio · game refinement theory · outcome predictability · win-rate separation ·
Elo resolution · games needed to distinguish players · noise threshold · collapse threshold ·
Lyapunov exponent in games · finite-size Lyapunov exponent · decision divergence ·
agent-free difficulty metric · level difficulty measure · solvability metric ·
controllability of an avatar · pen/cursor control · one-touch control

**Caveat, carried from the portfolio.** *Luck* and *difficulty* are both overloaded across
fields. A retrieval under either is **read before it is counted**, not counted on the title.

---

## 3. Venues and surfaces

**Indices.** dblp · arXiv (`cs.AI`, `cs.HC`, `cs.LG`, `cs.GT`) · OpenAlex · Google Scholar
**including its forward-citation graph.** The forward sweep is **mandatory, not optional** —
a skipped forward sweep is the single most common way a search misses the work that already
did this.

**Games venues.** IEEE CoG (and its predecessor **CIG** — the rename matters, pre-2019 work
is under CIG) · IEEE Transactions on Games (**ToG**, and its predecessor **TCIAIG** — same
issue) · FDG · AIIDE · CHI PLAY · DiGRA · Entertainment Computing · ICGA Journal ·
Game Studies · IEEE Transactions on Computational Intelligence and AI in Games.

**Spillover venues**, where the same result is often published without the word "game":
AAAI · IJCAI · NeurIPS · ICLR · AAMAS · CHI.

**One hand sweep is already scheduled and is not optional:** `CITATIONS.md` **O-7** — CoG,
FDG and AIIDE 2019–2025 for indirect-control papers, half a day, **blocking `canvascurse`'s
related-work section.** A tool sweep does not substitute for it.

---

## 4. Evidence tiers

Every retrieval carries a tier, and the tier travels with the claim.

| Tier | Meaning |
|---|---|
| **`[V]`** | Read in the original. The full text was opened and the relevant passage read. |
| **`[V-sub]`** | Partly verified — abstract or a specific section read in the original, the rest not. |
| **`[T]`** | Tool-extracted. A search snippet, an abstract from an index, a summary. **Not read.** |

**A `[T]` retrieval may not carry a novelty claim.** A `k` assembled from `[T]` retrievals is
reported as `[T]`-tier and the claim states so.

This is not bureaucracy. On 2026-08-16, **every literature claim in the portfolio that had not
been read in the original turned out to be wrong.** `FAILURE-MODES.md` F-1.

---

## 5. Cutoff, stopping rule, adjudication

- **Upper cutoff:** the run date, recorded in the archive header. Anything published after it
  is out of scope *for that run*; if it surfaces later it triggers a fresh run, never an
  amendment to the old one.
- **No lower cutoff.** Prior art in games is old and scattered — the game-refinement and
  skill/luck literatures predate the venues above by decades.
- **Stopping rule:** term-list exhaustion. **Not** saturation, **not** judgment, **not** "I
  found the answer."
- **Adjudication:** a retrieved work counts toward `k` if it asks the question *in any
  setting*. Setting mismatch — a board game where we study a platformer, a human study where
  we run agents — is recorded in the archive and reported in the "differs in Y" clause. It
  does **not** reduce `k`. **Ties are resolved against novelty.**

---

## 6. Archive and honesty clause

One file per run: `projects/<slug>/LITSEARCH-<YYYY-MM-DD>.md`, containing:

1. the run date and the claim under test;
2. **the exact queries issued** — not a description of them;
3. every retrieval, with its tier and its count decision;
4. the `k`, the nearest work, and the "differs in Y" statement;
5. — **required** — a **surfaces-not-reached** section: which venues, years, indices,
   languages and paywalls were not covered, and what would cover them.

**A run without the surfaces-not-reached section is not a completed run.**

The archive is written once and not edited. A second run is a second file.

---

## 7. What this protocol cannot do

It finds published work. It does not find:

- **licence and legal constraints** — the Rain World project died on the Akupara EULA
  (`CITATIONS.md` §1.4), which no literature sweep would ever have surfaced;
- **what a venue will actually accept** — both theory documents here warn that CoG rejects a
  dynamics paper wearing a games costume, and no search returns that;
- **whether the question is worth asking.**

`FAILURE-MODES.md` F-10 is the general form: review and search are both internal operations.
Some things require opening the actual thing.
