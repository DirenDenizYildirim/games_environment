# canvascurse

_You control the pen, not the character. Can level difficulty be measured agent-free, as a
budgeted-actuation quantity `ρ*`?_

| | |
|---|---|
| **Theory (authoritative)** | `~/MainIdeas/Theories/CanvasControl.md` (1920 lines, **v1.4**) |
| **Companions** | `~/MainIdeas/Supporting_Docs/CanvasControl_Formalization.md` · `_LitReview.md` · `_GameDesign.md` |
| **Ledger** | `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` §2, rows C-1…C-9 |
| **Citations** | `~/MainIdeas/Supporting_Docs/CITATIONS.md` §3.3 |
| **Venue** | IEEE CoG 2027 — full papers **1 Mar 2027** |
| **Status** | **active, ~3× over-scoped.** Sound theory, wrong size |

## What it claims

*Budgeted Geometric Actuation.* The player does not act on the agent; the player spends a
regenerating budget to alter the geometry the agent moves through. `ρ*` is the minimum
actuation budget at which a level is solvable — a difficulty measure that needs no agent, no
player model, and no playtest.

**Precedence, per v1.4 (ledger C-3):** **§4 is the paper. §5 is the method.** Versions
1.0–1.3 said the opposite. If a session finds itself leading with the mathematics, it has
reverted to v1.3.

Where the theory document and `CanvasControl_GameDesign.md` disagree on what a *designer*
should do, **the game design document wins.** Where they disagree on anything else, the
theory document wins. That precedence is stated in the theory document's own header.

## What is already established

- **The document did not drift, and it is the portfolio's evidence for why.** At 1920 lines
  it is more than twice APC's length, and APC drifted badly while this did not. The
  difference is that §1.2 keeps re-stating the two questions the project started from. A
  document that keeps saying *why it exists* does not drift; one that only says *what it now
  is*, does. `FAILURE-MODES.md` F-9.
- **§1.2 also contains the project's sharpest self-criticism**, unanswered across four
  versions: *"Swap the ball for a delivery drone and the ink for a beacon budget. Nothing in
  §2, §3 or §5 changes — not a symbol."* v1.4 exists to answer it. Whether it does is ledger
  **C-1**, and it is the venue question in one sentence.
- **§5.7 concedes the §5.9 machinery is standard beam optics** and that only the application
  is new. That is an honest concession and it is also a large share of §5's length
  (ledger **C-6**).
- Descends from `topics.md` **seed 1**, which it still answers. One of only two documents in
  the portfolio that can be said of.

## What is blocked

- **The related-work section**, on **O-7**: a hand sweep of CoG, FDG and AIIDE 2019–2025 for
  indirect-control papers. Half a day. A tool sweep does not substitute — that is exactly
  what `docs/SEARCH-PROTOCOL.md` §3 says about this item.

## The scope problem

Assessed at roughly **3× over-scoped** for a 1 March 2027 deadline. This is not a criticism of
the theory; it is a statement about twelve milestones and six months.

Ledger **C-7** is the problem in the document's own words: *"two papers, not one"* is stated
in §9 and then not done. The cut is a decision he makes, and until he makes it this project's
`BUDGET.md` cannot be filled in honestly.

## Where to start reading

1. `HANDOFF.md` here — always first.
2. **§14, the notation table.** Before your first substantive turn. `FAILURE-MODES.md` F-2.
3. **§1.2** — the two questions, and the self-diagnosis. Read it even if the work is in §5.
4. Then the section the handoff names. **Do not read all 1920 lines** — `PROTOCOL.md` §8.

For anything designer-facing, `CanvasControl_GameDesign.md` §6 is the design-image catalogue
that §5's results map onto. A §5 result with no §6 image is probably not worth its page.
