# BUDGET — canvascurse

_Compute and calendar ceiling. Read before any design. `FAILURE-MODES.md` F-3._

Every artifact that proposes something carries a budget line against this file. "Cost: none"
is almost always false, and no document in this portfolio has ever carried a calendar line —
which is how one of them reached fourteen months.

---

## 1. Compute

**Not yet costed, and that is the project's largest untracked risk.** The theory document
runs to 1920 lines across 12 milestones and has been assessed at roughly **3× over-scoped**
for the deadline, but no document in the portfolio carries a calendar or compute line
(`FAILURE-MODES.md` F-3).

Before any design work: cost the 12 milestones, mark which are mandatory for a single paper,
and record which are cut. Ledger row **C-7** — *"two papers, not one"* is stated in §9 and
then not done — is this problem in the theory document's own words.

The simulator is deterministic (ledger **C-9**), so cost is dominated by the planner and by
the size of the level sweep, not by physics.

**Per-rollout cost ceiling:** not yet derived. Deriving it is the first Tier 2 item in any
design session, because it is a constraint on the design rather than a consequence of it.

---

## 2. Calendar

| Milestone | Date | Slack |
|---|---|---|
| Code starts | Sept 2026 | — |
| CoG 2027 full papers | **1 Mar 2027** | ~6 months |

At ~3× over-scoped, the deadline is not met by this project as currently written. Either the
scope is cut or the venue moves. That is a decision, not a schedule problem.

---

## 3. What is verified and what is asserted

| Figure | Status |
|---|---|
| Any number in §1 not marked verified | **asserted** |

Keep this table honest. An asserted number that gets quoted three times starts reading as a
measurement.
