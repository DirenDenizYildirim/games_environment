---
name: build-memo
description: Write the Tier 2 build memo required by PROTOCOL.md §3.2 before any work on a declared surface, then stop. Use before starting Tier 2 work, and whenever the user types /build-memo.
---

# Build memo

Required before any Tier 2 work. `PROTOCOL.md` §3.2.

**Write the memo and stop. Do not write code in the same turn.** That rule is in `CLAUDE.md`
§6 and it exists because a memo written alongside its implementation is a description, not a
proposal — by the time it is read, the decision has been made.

## Format

```
## Build memo: <short name>
**Project:** <slug>
**Goal:** one line — what will be true after this that isn't now
**Approach:** 2–4 sentences, concrete
**Why this way:** alternatives considered, and why rejected
**Assumptions:** load-bearing ones, explicitly listed
**Choices this forces:** anything that becomes a DECISIONS_LEDGER row
**Touches:** files, interfaces, schemas affected
**Verification:** the actual test, not "it should work"
**Budget impact:** against projects/<slug>/BUDGET.md
**Tier:** 2 or 3
**Reversibility:** easy / painful / one-way
```

## The fields that carry the memo

**Why this way.** If you write *"this is the standard approach"*, you have not filled this
field in. Name what it is standard **for**, and say why this case matches. Two real
alternatives, rejected for stated reasons, or the field is empty.

**Assumptions.** Anything guessed because nobody knows. Each one gets an `ASSUMPTION:` marker
in the code and a row in `projects/<slug>/ASSUMPTIONS.md`. If you cannot name what would
validate an assumption, say that — an unvalidatable assumption is a finding in itself.

**Choices this forces.** Distinct from assumptions, and the field most often left blank. An
assumption is *guessed because nobody knows*; a **choice** is a fork where a different answer
was available and would change downstream work. Choices do not get made in a build memo —
they get logged as `DECISIONS_LEDGER.md` rows, unmarked, with no recommendation
(`PROTOCOL.md` §5.7). If this memo forces one, name it here and write the row.

**Verification.** *"Unit tests"* is not verification. Name the case, the expected value, and
where the expected value comes from. For any estimator, name the point it is evaluated at and
say why that point is **unfavourable** — `FAILURE-MODES.md` F-8 is a positive control sited
somewhere benign, and it is the most expensive silent failure in this discipline.

**Budget impact.** A number, against the project's `BUDGET.md`. *"Cost: none"* is almost
always false (F-3): check compute, schedule, claim strength, and any preregistration
commitment that could never be tuned again.

**Reversibility.** `one-way` means it cannot be undone without discarding data or breaking a
lock. Tagging a preregistration is one-way. Choosing an N ladder that data is then collected
against is one-way in practice.

## Before submitting

Run the `PROTOCOL.md` §3.3 trigger list against your own memo. If it proposes a claim change,
introduces or redefines a symbol, states a literature fact, carries a decision-gating number,
declares a cost of none, or proposes an acceptance criterion — **the memo itself needs a
red-team pass** before it is accepted. Use `/redteam`.

Then stop and wait.
