---
name: redteam
description: Run the mandatory adversarial review from PROTOCOL.md §3.3 against a written artifact — parallel lenses, then independent verification of each finding. Use when an artifact hits a §3.3 trigger, and whenever the user types /redteam.
---

# Red-team pass

`PROTOCOL.md` §3.3. Established after a session in which roughly half of ~20 proposed theory
amendments did not survive adversarial review, and **self-review caught none of them.**

## When it is required — syntactic, not a judgment call

An artifact needs a pass before acceptance if it does **any** of:

1. proposes a change to a claim, a hypothesis, or a preregistered value;
2. introduces or redefines a symbol, an axis, or a measured quantity;
3. **states a fact about the literature**;
4. **carries a number that gates a decision** — compute, `N`, a threshold, an effect size;
5. **declares a cost of "none", "zero", "free", or "negative"**;
6. proposes a new acceptance criterion or kill gate.

Items 3, 4 and 5 are the highest-yield. In the 2026-08-16 check, every unverified literature
claim was wrong and every "cost: none" was false.

## When it is not

**Do not run this on Tier 0/1 work, on code tests already cover, or on prose with no
load-bearing claim.** It is expensive. Blanket application turns it into ritual compliance and
it stops being read — which costs more than the tokens.

## Two hard preconditions

**1. Against a written artifact, never a plan in conversation.** The reviewer needs the actual
text; defects live in the wording, the arithmetic and the cross-references. If the thing does
not exist as a file, write it first.

**2. Name the suspected weak points in the brief.** Every high-value finding comes from a
specifically targeted question. Open-ended *"review this"* produces agreement and praise.

## Running it

`.claude/workflows/redteam.js` does this end-to-end. To run it by hand:

**Stage 1 — lenses, in parallel, one message.** Four distinct lenses, each told what the
others cover so they do not overlap:

| Agent | Lens |
|---|---|
| `redteam-technical` | derivations, definitions, symbol usage, estimator construction |
| `redteam-quantitative` | numbers, costs, budgets, `N`, effect sizes, "cost: none" |
| `redteam-consistency` | contradictions, cross-references, stale versions, unadopted self-diagnoses |
| `redteam-designer` | design consequence, the substitution test, venue fit |

Each is instructed to **omit everything that is fine.** Praise dilutes signal and costs
context.

**Stage 2 — verify every finding independently.** One `finding-verifier` per finding, in
parallel. This half is **not optional**:

> **Red-team findings are claims, not verdicts.** Reviewers are right roughly 85% of the time.
> Adopting reviewer output on authority replaces one unchecked source with another — which is
> the failure the review exists to prevent.

Verdicts are `CONFIRMED` / `PLAUSIBLE` / `REFUTED`. A finding resting on a `[T]`
(tool-extracted, unread) literature retrieval is **at best `PLAUSIBLE`**.

**Stage 3 — record the outcome in the artifact itself.** What was found, what was verified,
what was withdrawn, and by which lens. A later reader must be able to see which parts have
been tested and which have not. **An artifact that has not been reviewed says so explicitly.**

## What this cannot catch

`FAILURE-MODES.md` **F-10**. Red-teaming is strong at internal consistency and has caught
**none** of: a platform contradiction, a prohibitive EULA, an export-control category, a
conflated citation, or a self-diagnosis that survived four document versions. All of those
needed **external contact** — opening a source, checking a licence, running a search.

A clean pass is evidence the artifact is internally consistent. It is not evidence it is
right. After any clean pass, ask the three questions in F-10.
