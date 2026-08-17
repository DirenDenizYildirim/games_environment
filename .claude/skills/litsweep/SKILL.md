---
name: litsweep
description: Run the declared pre-emption search from docs/SEARCH-PROTOCOL.md against a specific claim, and archive the result as a LITSEARCH file with its surfaces-not-reached section. Use before any novelty claim, and whenever the user types /litsweep.
---

# Literature sweep

`docs/SEARCH-PROTOCOL.md` is the authority. This skill runs it.

The output is a **reported number, not a verdict.** Nothing passes or fails on it.

## Before starting

**State the claim under test, in one sentence.** A sweep against "the project" returns
everything and settles nothing. A sweep against *"the collapse threshold is predictable from
game structure with functional form X"* returns something you can adjudicate.

## The five rules

1. **Exhaust the term cross-product.** Every term in group A crossed with every term in group
   B; group C run flat. The stopping rule is **exhaustion**, not saturation, not judgment, and
   emphatically not "I found the answer."
2. **Record queries verbatim.** The archive must be re-runnable by someone else.
3. **Tier every retrieval honestly.** `[V]` read in the original · `[V-sub]` partly read ·
   `[T]` tool-extracted, not read. Most will be `[T]`. **That is fine as long as it says
   `[T]`** — and a `[T]` retrieval may not carry a novelty claim.
4. **Forward-citation sweep is mandatory.** For every close retrieval, follow who cited it.
   The work that already did this is more often a citer of the nearest paper than the nearest
   paper itself.
5. **Ties resolve against novelty.** A work counts toward `k` if it asks the question in
   **any** setting. Setting mismatch is recorded and reported in the "differs in Y" clause; it
   does not reduce `k`.

## Running it

`.claude/workflows/litsweep.js` fans slices out across `lit-sweeper` agents. By hand: one
`lit-sweeper` per term pair, in parallel, then assemble.

## Assembling the result

```
This question has been asked in **k** retrieved works; the nearest is **X**;
our claim differs in **Y**.
```

`k = 0` is legitimate and **weak**. It is not evidence of novelty — it is the absence of
evidence against it, over a bounded surface, quantified and auditable. Report it that way.

## The archive

One file per run: `projects/<slug>/LITSEARCH-<YYYY-MM-DD>.md`.

```markdown
# LITSEARCH — <project> — YYYY-MM-DD

**Claim under test:** one sentence
**Upper cutoff:** the run date. Anything later is out of scope for this run.
**Protocol version:** docs/SEARCH-PROTOCOL.md as of <commit>

## Queries issued
## Retrievals            (work | tier | counts toward k | why / setting mismatch)
## Forward-citation sweep
## Result                (k, nearest, differs in Y, and the tier of the k)
## Surfaces not reached  ← REQUIRED
```

**A run without the surfaces-not-reached section is not a completed run.** Paywalls, 403s,
languages, years, indices you could not reach — all of it, with what would reach it. This
portfolio's open-items list is largely made of these, and every one of them is honest rather
than embarrassing.

**Write once. Do not edit.** A second run is a second file — including a survivor sweep
against a narrowed claim, which is a second run.

## After the sweep

- If it kills a framing, that is the sweep working. Both robotics projects had a headline
  taken and both are better for finding out before writing code.
- **Consider a second sweep against the survivors.** `chaos-luck` ran one and it corrected its
  own K1: the first sweep's "was not found" was wrong, and the second produced the best
  positioning the project has.
- **A restructure forced by evidence is not a decision made.** Log it as a
  `DECISIONS_LEDGER.md` row with the live options enumerated and **none marked** —
  `/ledger-row`. Rows CR-11, LK-7 and LK-8 are exactly this shape.
- Update `CITATIONS.md` §4 with anything you could not reach.
