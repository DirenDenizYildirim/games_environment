---
name: session-end
description: Run the session-end ritual from PROTOCOL.md §2.3 — overwrite HANDOFF.md and update the other state documents that earned an entry. Use before ending any session in this repo, and whenever the user types /session-end.
---

# Session end

`PROTOCOL.md` §2.3. **`HANDOFF.md` gets written every session, no exceptions.** Everything
else gets written only when it earned it.

## 1. `projects/<slug>/HANDOFF.md` — always

**Overwrite completely.** State, not history. Under one page — a handoff that grows without
bound stops being read, which defeats it.

```
# HANDOFF — <project>
_Last session: YYYY-MM-DD | branch | commit_

## Current state          — where the project actually is, 3–5 lines
## In flight              — what is half-done, and precisely where it stops
## Blocked                — what cannot proceed, and what unblocks it
## Next actions           — ordered, specific enough to start without asking
## Open questions         — things he must decide
## Traps for next session — non-obvious behaviour, known-failing tests, do-not-touch config
```

**"In flight" is the field that matters.** *"Half-done"* is useless; *"the estimator is
written and passes S1–S3, S4 fails and I believe it is the tie-breaking rule in
`rank()`"* is a handoff. Write the second kind.

**"Traps" is the second-most-valuable field** and the one most often left empty. Anything that
cost you fifteen minutes to discover goes here.

## 2. `DIARY.md` — only when it earned it

A dated entry **only** if the session produced something a future reader would want narrated:
a surprise, a dead end, a changed belief, a discovered coupling, a result.

Mechanical execution of an approved plan with no surprises gets **one line**.

**Do not write an entry that restates the TODO list.** If it contains nothing a reader could
not reconstruct from `git log`, it should not exist. Padding destroys the file's value, and
`CLAUDE.md` §6 names it explicitly.

```
## YYYY-MM-DD
**Did:** brief
**Surprised by:** what didn't match expectation — the important field
**Changed my mind about:** if applicable
**Dead end:** what was tried and abandoned, and why — so nobody retries it
**Unresolved:** what is still nagging
```

## 3. `DECISIONS.md` — one entry per Tier 2/3 decision made this session

None made → **do not touch the file.** Format in `PROTOCOL.md` §5.3. Fill in `Revisit if`
properly; it is what makes the file more than documentation.

## 4. `RISKS.md` — changes only

New risks, status changes, retirements. **Nothing changed → append a dated line saying so.**
That is itself information: it records that the register was looked at.

Retire explicitly when a risk is dead. A register that only grows is noise.

## 5. `ASSUMPTIONS.md` — every new marker

Every `ASSUMPTION:` marker written this session has a row. The pre-publication audit greps the
code and diffs against this file; a mismatch in either direction is a defect.

## 6. `DECISIONS_LEDGER.md` — every load-bearing choice surfaced

At `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md`. Use `/ledger-row`.

A choice is a fork where **a different answer would change downstream work.** Not every design
detail. If this session settled one — a parameter, a formalization, a framing, a scope
boundary — it becomes a row: unmarked, no recommendation. `PROTOCOL.md` §5.7.

**This is the step most likely to be skipped and the most expensive to skip.**

## 7. Report

Four things, briefly:

- what got done;
- what is blocked;
- what you would do next;
- **what you are least confident about.**

The last one is not decoration. It is the thing the next session most needs and the thing a
clean summary hides.

## When to end early

If the session has run long, or you notice you are re-deriving something established earlier:
**stop, write the handoff, and propose a fresh session.** `PROTOCOL.md` §8. A clean handoff
beats a degraded continuation, and this is an explicitly legitimate reason to stop.
