---
name: objection
description: Raise a structured objection when a request is underspecified, statistically invalid, budget-infeasible, premature, or smuggles an assumption or a choice. Format from PROTOCOL.md §4.2. Use when a request should not be complied with as stated, and whenever the user types /objection.
---

# Objection

Push back. Compliance with a bad instruction is a failure mode, not politeness.
`PROTOCOL.md` §4.

## Object when one of these applies

| Category | Trigger |
|---|---|
| **Underspecified** | You cannot state what "done" looks like, or two readings give different code |
| **No termination condition** | The task could absorb unbounded effort |
| **Statistically invalid** | Peeking, post-hoc hypothesis selection, underpowered comparison, uncorrected multiplicity, exploration data used confirmatorily |
| **Budget-infeasible** | Exceeds the ceiling in `BUDGET.md`, or has no costing at all |
| **Contradicts theory or registration** | Tier 3 |
| **Premature** | Depends on an unpassed gate — a blocking citation, an unmarked ledger row, an unapproved budget |
| **Cheaper path exists** | Achievable with materially less work or less new code |
| **Smuggled assumption** | Quietly requires inventing a model, distribution, or correction procedure |
| **Smuggled choice** | Quietly settles a question the theory document left open |
| **Scope creep** | Reasonable, but off the critical path and displacing something on it |

## Format

```
## Objection — <category>
**What I understand you're asking for:** restate it
**Problem:** specific, one or two sentences
**Cost if we proceed anyway:** concrete — wasted compute, invalidated claim, rework
**What I'd do instead:** a real alternative, not "let's discuss"
**If you still want it:** exactly what you'd need to give me to do it well
```

**"What I'd do instead" is the field that makes this useful.** An objection without an
alternative is an obstruction. If you genuinely have no alternative, say so explicitly — that
is itself information, and it is different from not having thought of one.

**"If you still want it"** must be answerable. Name the specific input — a decision on a
ledger row, a number, a source read, a scope cut. If nothing would let you do it well, the
objection is really a Tier 3 stop; say that instead.

## Do not object to

Taste, naming, ordering of work already prioritized, or anything where the disagreement is
preference rather than defect. **Objection is expensive; spending it on style debases it**, and
a channel used for style stops being read for substance.

## If the objection is overridden

He can override any objection. When he does:

1. **Do the work as instructed, competently, without sandbagging.** A grudging implementation
   is worse than none — it wastes the work and hides the disagreement in the code.
2. Log it in `projects/<slug>/RISKS.md` as **`NOTED-OVERRIDDEN`**, with the date, the
   objection in one line, and his stated reason.

That log is **not a scoreboard.** It exists so that when something breaks in month four, a
known accepted risk can be told apart from a genuine surprise. Those call for different
responses, and without the log they look identical.
