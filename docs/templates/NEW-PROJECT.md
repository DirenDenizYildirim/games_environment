# Adding a project

A project directory is nine files. Create all nine — a missing one is not "not needed yet,"
it is a gap the session protocol will silently step over.

```
projects/<slug>/
├── README.md            what this is, and where its theory lives
├── HANDOFF.md           state, overwritten every session
├── SURFACES.md          the Tier 2 list — write this BEFORE the first line of code
├── DECISIONS.md         why the code is like this (indexed, append-only)
├── RISKS.md             live register
├── DIARY.md             narrative, append-only
├── ASSUMPTIONS.md       one row per ASSUMPTION: marker
├── PREREGISTRATION.md   stub until the project earns it; Tier 3 once tagged
└── BUDGET.md            compute and calendar ceiling
```

Then:

1. Add a row to `docs/PORTFOLIO.md` §2, with venue, gate state, and the live tensions.
2. Add a section to `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` if the project does
   not have one, with the choices already embedded in its theory document — **unmarked**.
3. Confirm the theory document exists in `~/MainIdeas/Theories/` and the relative path in
   `README.md` resolves. Run `ls` on it; do not assume.

---

## The order that matters

**`SURFACES.md` before code, not after.** It is the file the tier gate reads. Written after
the fact, it describes what was built; written first, it decides what needs approval. Those
are different documents with the same name.

**`PREREGISTRATION.md` before data, not after.** A stub is honest. A file filled in after
seeing results is not a preregistration regardless of what it says at the top.

**`BUDGET.md` before design.** `FAILURE-MODES.md` F-3: no document in this portfolio has ever
carried a calendar line, and the one project that grew unbounded grew because nothing costed
it.

---

## Formats

Every format is in `docs/PROTOCOL.md` §5. Do not invent a variant. The skeletons below are
the minimum content for a new project — copy, then fill.

### `README.md`

```markdown
# <project>

_One sentence: the question._

| | |
|---|---|
| **Theory (authoritative)** | `~/MainIdeas/Theories/<file>.md` |
| **Ledger** | `DECISIONS_LEDGER.md` §N, rows X-1…X-n |
| **Citations** | `CITATIONS.md` §N |
| **Venue** | |
| **Status** | active / deferred / blocked |

## What it claims
## What is already established
## What is blocked
## Where to start reading
```

### `HANDOFF.md`

`PROTOCOL.md` §5.1. Six headings, under one page, overwritten entirely each session.

### `SURFACES.md`

`PROTOCOL.md` §5.8. Three tables. The third — **explicitly NOT Tier 2** — is not optional;
without it the list inflates until the gate becomes ritual.

### `DECISIONS.md`

`PROTOCOL.md` §5.3. Starts with an empty index and the sentence *"No decisions yet."*

### `RISKS.md`

`PROTOCOL.md` §5.4. Seed it from the theory document's own threat list — those documents all
have one, and it is better than anything written from scratch.

### `DIARY.md`

`PROTOCOL.md` §5.2. Starts empty. **Do not seed it.** A diary with invented entries is worse
than no diary.

### `ASSUMPTIONS.md`

`PROTOCOL.md` §5.6. Table with columns: ID · What was assumed · Where the marker is · What
would validate it · Status.

### `PREREGISTRATION.md`

`PROTOCOL.md` §5.5. Until the project earns one, the file contains the section skeleton and a
banner saying **STUB — NOT LOCKED**, so nobody mistakes a template for a commitment.

### `BUDGET.md`

Compute ceiling, the derived per-unit cost constraint, and the calendar. State what is
*verified* and what is *asserted* — the portfolio's `$120 rented card` figure has never been
checked against a real design.
