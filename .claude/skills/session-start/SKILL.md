---
name: session-start
description: Run the session-start ritual from PROTOCOL.md §2.1 — establish the active project, read its state documents, and produce a tiered TODO list. Use at the beginning of every session in this repo, before any other work, and whenever the user types /session-start.
---

# Session start

`PROTOCOL.md` §2.1. Do this before anything else, including before answering what looks like a
simple question. The cost is two minutes; the cost of skipping it is working against a stale
picture of the project.

## Steps, in order

**1. Establish the active project.**
List `projects/`. Most requests name one project. If the request touches more than one, say so
and pick the primary — a session that drifts between projects writes two half-handoffs and
neither is usable.

**2. Read the state documents** for that project, in this order:

| File | Read | Why |
|---|---|---|
| `projects/<slug>/HANDOFF.md` | **in full** | current state of the world |
| `projects/<slug>/SURFACES.md` | **in full** | you cannot classify a tier without it |
| `projects/<slug>/DECISIONS.md` | **index only** | context budget — pull entries on demand |
| `projects/<slug>/RISKS.md` | **in full** | check whether anything active touches today's request |
| `docs/PORTFOLIO.md` | **skim** | what changed around the project since the handoff |

Do **not** read the theory document yet. It is 578 or 1920 lines and the handoff tells you
which section you actually need.

**3. Check the tree.** `git status`, branch, last commit. If the repo is not a git repo yet,
say so once — it should be one before any code exists.

**4. Report, in two or three lines.** Where the project is, what is blocked, and anything in
`RISKS.md` that today's request touches. Not a summary of what you read.

**5. Produce the TODO list.** Before writing or modifying anything.

## The TODO list

Each item states three things:

```
N. <what it is>  — Tier <0|1|2|3> — done means: <the concrete condition>
```

Order by dependency. Mark an item **blocked** rather than working around it if it depends on:

- an unread blocking citation (`CITATIONS.md` §4 — e.g. O-17, O-14, O-7);
- an unmarked ledger row with large blast radius;
- an unapproved budget;
- a Tier 3 decision that has not been made.

**Then apply the gate:**

- Every item Tier 0 or Tier 1 → **proceed.** Tier 1 items get a one-paragraph note as you
  reach them. Do not wait for approval.
- Any item Tier 2 or Tier 3 → **present the list, stop, and wait.**

Use `/tier-check` if a classification is not obvious. When two tiers are arguable, take the
higher one — misclassifying downward is the expensive error.

## What this is not

It is not a summary of the project for the user's benefit; they wrote these documents. It is
you loading the state you need to not repeat work, not re-derive settled things, and not walk
into a known trap. The `Traps for next session` section of the handoff exists for exactly
this and is the highest-value part of it.
