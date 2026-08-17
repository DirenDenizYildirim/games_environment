---
name: ledger-row
description: Log a load-bearing research choice as an unmarked row in MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md instead of adopting it. Use whenever work settles a question a theory document left open, and whenever the user types /ledger-row.
---

# Ledger row

**The rule the whole repo exists to serve.** `PROTOCOL.md` §5.7.

When work reaches a fork where a different answer would change downstream work, that is
**his** to decide. It gets **logged**, not adopted.

## Where

`~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` — outside this repo, because it spans
every project including ones with no repo. Append to the project's section; create one if the
project does not have it.

## What qualifies

A choice where **a different answer would change downstream work.** Not every design detail —
only what other things get built on top of.

| Goes in the ledger | Goes straight into the work |
|---|---|
| A formalization | A finding |
| An invented parameter | A bug fix |
| A framing or a venue | An implementation detail with no downstream effect |
| A scope boundary | Something the theory document already decided |
| A word in the title | A typo |
| A recommendation | A measurement |

If you are unsure, log it. An unnecessary row costs one line; an unlogged choice cost this
portfolio a fourteen-month hardware programme nobody chose.

## The row

```
| <ID> | **<the choice, stated flatly>** | <where it lives> | <what changes if it changes> | ☐ |
```

## Four rules, all load-bearing

**1. No recommendation.** The "if it changes" column is a **factual statement about what
depends on the choice.** Which way to decide is not yours to write down. The ledger's own
header says so: *"This file contains no recommendations."*

**2. The mark column stays empty — `☐`.** `C` (he chose it) / `A` (it appeared) / `?` are his
marks. **Never fill one in.** The marks are the entire mechanism: they are how he finds the
decisions that were made for him.

**3. State it as a choice, not as an assumption the reader has to catch.** *"Hazards are
implemented as channel masks"* — not a paragraph that quietly uses masks and never says so.

**4. When evidence forces a restructure, that is still not a decision.** Enumerate the live
options and mark none. Say explicitly *"forced by evidence, not chosen — but which way to
restructure is still a choice."* Rows CR-11, LK-7 and LK-8 are the model.

## Also worth marking

**⚑** if the theory document **already questions itself** on this point — an open question, a
stated threat, a self-diagnosis. Those are pre-flagged, not pre-answered, and they are the
cheapest rows for him to resolve.

## Why this exists

The APC theory document grew from an eleven-line seed targeting a workshop paper to 805 lines
and a fourteen-month hardware programme, having silently adopted **aerial drones** — a
platform contradicting its own §12. It surfaced months later through an unrelated
export-control check. He named it *"the curse of AI writing my theory doc."*

Every row you write is one instance of that not happening again.

## After writing

Mention the row in the session report — ID, one line, and its blast radius. Do not summarise
what you think he should decide.
