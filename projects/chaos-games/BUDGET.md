# BUDGET — chaos-games

_Compute and calendar ceiling. Read before any design. `FAILURE-MODES.md` F-3._

Every artifact that proposes something carries a budget line against this file. "Cost: none"
is almost always false, and no document in this portfolio has ever carried a calendar line —
which is how one of them reached fourteen months.

---

## 1. Compute

The compute figure is **derived, not chosen**. Ledger row **G-11** fixes δ = 0.05, which
sets M ≈ 785 matches per condition; **G-6** sets 8–12 games; **G-10** makes noise-aware vs
noise-blind a headline factor, which **doubles** the match count rather than adding a
robustness check. The theory document's ~10⁶-match figure falls out of those three rows.

**Any change to δ, to the game count, or to the noise-aware factor is a budget change** and
gets costed here before it is agreed anywhere else.

**TAG is JVM.** The `topics.md` plan — JAX on a rented 5090, ~$120 — belongs to the robotics
seed and buys this project nothing (ledger **G-7**). Do not import that number.

**Per-match cost ceiling:** not yet derived. Deriving it is the first Tier 2 item in any
design session, because it is a constraint on the design rather than a consequence of it.

---

## 2. Calendar

| Milestone | Date | Slack |
|---|---|---|
| Code starts | Sept 2026 | — |
| CoG 2027 full papers | **1 Mar 2027** | ~6 months |

Ledger **X-2**: the theory document scopes at more than six months. That gap is real and is
closed by cutting scope, not by working faster.

---

## 3. What is verified and what is asserted

| Figure | Status |
|---|---|
| Any number in §1 not marked verified | **asserted** |

Keep this table honest. An asserted number that gets quoted three times starts reading as a
measurement.
