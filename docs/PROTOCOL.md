# PROTOCOL — full operating protocol

The short form is the repo-root `CLAUDE.md`, auto-loaded every session. This file holds the
detail. Read a section when the root file points you here.

This protocol is **project-agnostic by construction**. Nothing in it names a claim, an
estimator, or a hypothesis. Anything project-specific lives in `projects/<slug>/` — and the
one file that makes the tier system work, `SURFACES.md`, is written per project (§5.8).

---

## 1. Prime directives

Stated in full in root `CLAUDE.md` §1 and not duplicated here — that file is auto-loaded
every session, so the directives are always in context and this file must not carry a second
copy that can drift.

---

## 2. Session protocol

### 2.1 At session start — always, before anything else

The `/session-start` skill runs this. Do it in order and report the result in two or three
lines. Do not skip because the request seems simple.

1. **Establish which project is active.** Most requests name one. If the request touches
   more than one, say so and pick the primary — a session that drifts between projects
   writes two half-handoffs and neither is usable.
2. Read `projects/<slug>/HANDOFF.md` in full. This is the current state of the world.
3. Read `projects/<slug>/SURFACES.md`. You cannot classify a request into a tier without it.
4. Read the **index** at the top of `projects/<slug>/DECISIONS.md` (not the whole file).
5. Read `projects/<slug>/RISKS.md` — check whether anything active touches today's request.
6. Skim `docs/PORTFOLIO.md` for calendar or gate changes since the handoff was written.
7. Confirm the working tree is clean; note the branch and last commit.
8. **Produce a TODO list** before writing or modifying anything.

Each TODO item states: what it is, its tier, and what "done" means. Order by dependency.
If an item depends on an ungated decision — an unread blocking citation, an unmarked ledger
row with large blast radius, an unapproved budget — mark it **blocked** rather than working
around it.

**Then:**
- Every item Tier 0 or Tier 1 → proceed. Tier 1 items get their one-paragraph note as you
  reach them; you do not wait.
- Any item Tier 2 or Tier 3 → present the list, stop, and wait.

### 2.2 During the session

- One TODO item at a time. Do not batch Tier 2 items into one approval request.
- If the plan turns out to be wrong, stop and say so. Do not silently re-plan. A revised
  TODO list is cheap; discovering at session end that you built something other than what
  was approved is not.
- When you hit an assumption you cannot resolve from the repo or the theory document: mark
  it, log it in `ASSUMPTIONS.md`, and ask. Do not pick a plausible default and continue.
- When you hit a **choice** rather than an assumption — a fork where a different answer
  would change downstream work — that is a ledger row, not a decision to make. §5.7.
- Keep a running note of anything that surprised you. Surprises are the raw material for
  `RISKS.md` and often for `DIARY.md`.

### 2.3 At session end — always

The `/session-end` skill runs this.

1. **`projects/<slug>/HANDOFF.md`** — overwrite completely. State, not history. Format §5.1.
2. **`DIARY.md`** — dated entry only if the session produced something a future reader would
   want narrated. Mechanical execution of an approved plan with no surprises gets one line.
   Padding destroys the file's value.
3. **`DECISIONS.md`** — an entry per Tier 2/3 decision. None made → do not touch.
4. **`RISKS.md`** — new risks, status changes, retirements. Nothing changed → append a dated
   line saying so; that is itself information.
5. **`ASSUMPTIONS.md`** — every new `ASSUMPTION:` marker written this session has a row.
6. **`DECISIONS_LEDGER.md`** — every load-bearing choice surfaced this session has a row,
   unmarked, with no recommendation. §5.7.
7. Report: what got done, what is blocked, what you would do next, what you are least
   confident about.

---

## 3. The work gate

### 3.1 Tiers

The tier table is in root `CLAUDE.md` §2. Three clarifications that belong here:

**Tier 2 is defined by a list, not by feeling.** The list is `projects/<slug>/SURFACES.md`,
written when the project starts and amended only by a Tier 2 decision of its own. "Is this
big?" is not the question. "Is it on the list?" is. If a request touches something that
plainly should be on the list and is not, adding it is the first TODO item.

**Tier 3 triggers** are: changing any value in `PREREGISTRATION.md` after its tag;
contradicting a theory document in `~/MainIdeas/Theories/`; **editing** one at all;
choosing a statistical procedure the registration does not name; and anything involving
human subjects. Domain-specific additions are listed in root `CLAUDE.md` §2.

**Theory documents are read-only from this repo.** They are the authoritative statement of
what the project claims, they live in `~/MainIdeas/Theories/`, and a hook blocks writes to
them. When work here implies a theory document is wrong, that is a finding to report and a
ledger row to write — not an edit to make.

### 3.2 Build memo format

Before any Tier 2 work. The `/build-memo` skill emits this.

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

"Why this way," "Assumptions," and "Budget impact" are the fields that matter. If you find
yourself writing "this is the standard approach," that is not a reason — name what it is
standard *for* and why this case matches.

Then stop. **Do not write code in the same turn as the memo.**

### 3.3 Mandatory adversarial review

Carried over from the parent protocol, where roughly half of ~20 theory amendments proposed
in one session did not survive adversarial review, and self-review caught none of them.
`docs/FAILURE-MODES.md` has the recurring patterns and their detectors.

**The trigger is syntactic, not a judgment call.** A red-team pass is **required** before an
artifact is accepted if it does any of the following:

1. proposes a change to a claim, a hypothesis, or a preregistered value;
2. introduces or redefines a symbol, an axis, or a measured quantity;
3. states a fact about the literature;
4. carries a number that gates a decision — compute, `N`, a threshold, an effect size;
5. declares a cost of "none", "zero", "free", or "negative";
6. proposes a new acceptance criterion or kill gate.

Items 3, 4 and 5 are the highest-yield: in the 2026-08-16 check every unverified literature
claim was wrong, every "cost: none" was false, and the headline compute figure was wrong in
both directions.

**How to run it.** The `/redteam` skill and `.claude/workflows/redteam.js` implement this.

- **Against a written artifact, never a plan in conversation.** The reviewer needs the actual
  text; defects live in the wording, the arithmetic, and the cross-references.
- **Lenses are distinct and run in parallel** — technical correctness, quantitative and cost
  claims, internal consistency and cross-reference integrity, plus this repo's fourth lens
  (`redteam-designer`). Redundant reviewers produce agreement, which is worthless.
- **Name the suspected weak points in the brief.** Every high-value finding comes from a
  specifically targeted question. Open-ended "review this" produces praise.
- **Instruct the reviewer to omit anything that is fine.** Praise dilutes signal and costs
  context.

**How to accept it — this half is not optional.**

> **Red-team findings are claims, not verdicts.** Reviewers were right roughly 85% of the
> time. **Independently verify a finding before acting on it** — recompute the arithmetic,
> enumerate the set, check the citation in the original. Adopting reviewer output on
> authority replaces one unchecked source with another, which is the failure the review
> exists to prevent. The `finding-verifier` agent exists for this and its verdict is
> `CONFIRMED` / `PLAUSIBLE` / `REFUTED`, never a rewrite.

Record the outcome in the artifact itself — what was found, what was verified, what was
withdrawn. An artifact that has *not* been reviewed says so explicitly.

**Cost discipline.** This is expensive. It is justified for the triggers above and is **not**
to be applied to Tier 0/1 work, to code tests already cover, or to prose with no load-bearing
claim. Blanket application turns it into ritual compliance and it stops being read.

### 3.4 What red-teaming does not catch

The portfolio's own record (ledger row X-4): red-teaming is genuinely strong at internal
consistency and caught **none** of the platform contradiction, the prohibitive EULA, the
export-control category, a conflated citation, or a self-diagnosis that survived four
document versions unaddressed. Those all needed **external contact** — reading a source,
checking a licence, running a search. Do not let a passed review substitute for one.

---

## 4. Objection protocol

Push back. Compliance with a bad instruction is a failure mode, not politeness.

### 4.1 Object when any of these apply

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
| **Smuggled choice** | Quietly settles a question the theory document left open — §5.7 |
| **Scope creep** | Reasonable, but off the critical path and displacing something on it |

### 4.2 Objection format

The `/objection` skill emits this.

```
## Objection — <category>
**What I understand you're asking for:** restate it
**Problem:** specific, one or two sentences
**Cost if we proceed anyway:** concrete — wasted compute, invalidated claim, rework
**What I'd do instead:** a real alternative, not "let's discuss"
**If you still want it:** exactly what you'd need to give me to do it well
```

### 4.3 Overrides

He can override any objection. When he does: do the work as instructed, competently, without
sandbagging — and log it in `RISKS.md` as `NOTED-OVERRIDDEN` with the date, the objection,
and the stated reason.

That log is not a scoreboard. It exists so that when something breaks in month four we can
tell a known accepted risk from a genuine surprise. Those call for different responses.

### 4.4 Do not object to

Taste, naming, ordering of work already prioritized, or anything where the disagreement is
preference rather than defect. Objection is expensive; spending it on style debases it.

---

## 5. Document formats

### 5.1 `HANDOFF.md` — state, overwritten every session

*If a fresh session starts tomorrow with no memory, what does it need to know?*

Overwrite entirely. No history. Under one page — a handoff that grows without bound stops
being read, which defeats it.

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

### 5.2 `DIARY.md` — narrative, append-only

*What happened, and what did we learn?*

The only place uncertainty, dead ends, and things that felt wrong get recorded. Those are the
entries with long-term value — a clean summary of what worked is already in the commit log.

**Do not write an entry that restates the TODO list.** If it contains nothing a reader could
not reconstruct from `git log`, it should not exist.

```
## YYYY-MM-DD
**Did:** brief
**Surprised by:** what didn't match expectation — the important field
**Changed my mind about:** if applicable
**Dead end:** what was tried and abandoned, and why — so nobody retries it
**Unresolved:** what is still nagging
```

### 5.3 `DECISIONS.md` — code theory, append-only

*Why is the code like this?*

One entry per Tier 2/3 decision **made inside this repo**. Never edit an old entry —
supersede it with a new one referencing the old ID. Maintain the one-line index at the top;
that index is what gets read at session start.

```
### D-000X — <title>
**Date:** | **Status:** proposed | active | superseded by D-00XX
**Context:** what forced a decision
**Decision:** what we did
**Alternatives rejected:** and why — this field is the whole point
**Assumptions this rests on:** load-bearing ones, with how to check them
**Consequences:** what this makes easy, what it makes hard
**Revisit if:** the concrete condition that would invalidate this
```

`Revisit if` is what makes this file more than documentation. Fill it in properly.

**This file is not `DECISIONS_LEDGER.md`.** See §5.7 — they hold different things and
confusing them is how research choices get made by accident.

### 5.4 `RISKS.md` — live register

*What is most likely to make this project fail, and are we watching it?*

Each risk carries a status and a trigger. Retire explicitly — a register that only grows is
noise. `ACTIVE` / `WATCHING` / `MATERIALIZED` / `RETIRED` / `NOTED-OVERRIDDEN`.

### 5.5 `PREREGISTRATION.md` — locked

Hypotheses, thresholds, effect sizes, allocation rule, analysis plan, per-condition N.
Git-tagged. **Tier 3.** The analysis entrypoint verifies the file hash against the tag and
refuses to run on mismatch. If that check fails, do not disable it — stop and report.
Mechanism: SHA-256 of the file bytes, recorded in the annotated tag message and copied into
every run manifest as `prereg_hash`.

Until a project reaches that point the file is a **stub** and says so. A stub is not a lock;
filling it in is Tier 2, tagging it is Tier 3.

### 5.6 `ASSUMPTIONS.md` — ledger

One row per `ASSUMPTION:` marker in the code, with status. The pre-publication audit greps
the code and diffs against this file; unmatched entries in either direction are defects.

### 5.7 `DECISIONS_LEDGER.md` — the portfolio ledger, and the rule behind it

Lives at `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md`, outside this repo, because it
spans every project including ones with no repo.

**What goes in it:** a choice where *a different answer would change downstream work* — a
formalization, a parameter, a framing, a venue, a scope boundary, a word in the title. Not
every design detail. Only what other things get built on top of.

**How a row is written:**

```
| CR-15 | **<the choice, stated flatly>** | <where it lives> | <what changes if it changes> | ☐ |
```

Four rules, all of them load-bearing:

1. **No recommendation.** Blast radius is a factual statement about what depends on the
   choice. Which way to decide is not yours to write down.
2. **The mark column stays empty.** `C` (he chose it) / `A` (it appeared) / `?` are his
   marks. Never fill one in.
3. **State it as a choice, not as an assumption the reader has to catch.** "Hazards are
   channel masks" — not a paragraph that quietly uses masks and never says so.
4. **Findings and bug fixes do not go here.** They go straight into the work. Only
   recommendations and invented parameters get logged instead of adopted.

**Why this rule exists.** The APC theory document grew from an eleven-line seed to 805 lines
and a fourteen-month hardware programme, and had silently adopted aerial drones — a platform
contradicting its own §12. It surfaced only through an unrelated export-control check. He
named it *"the curse of AI writing my theory doc."* The ledger is the mechanism that stops
it recurring: choices become visible and unmarked, rather than invisible and settled.

**Size is not the drift signal.** `CanvasControl.md` is more than twice APC's length and did
not drift, because its §1.2 keeps re-stating the two questions the project started from. A
document that keeps saying *why it exists* does not drift; one that only says *what it now
is*, does. That is what `/drift-check` tests.

### 5.8 `SURFACES.md` — the project's Tier 2 list

The file that makes the tier system executable. Without it, "Tier 2" is a judgment call and
the gate does not hold.

```
# SURFACES — <project>
_Amending this list is itself Tier 2._

## Tier 2 surfaces
| Surface | Why it is Tier 2 | Named in |
|---|---|---|

## Tier 3 additions beyond the standard set
| Trigger | Why |
|---|---|

## Explicitly NOT Tier 2
| Thing | Why it is fine to just do |
|---|---|
```

The third table matters as much as the first. Without it the list inflates until everything
needs approval, which is how a gate becomes ritual and stops being read.

---

## 6. Epistemic rules

Expanded from root `CLAUDE.md` §4.

**The exploration/confirmation boundary.** Two modes, one core: `explore` (low N, many
conditions, no claims) and `confirm` (powered N, preregistered, claims).

- Exploration may inform: which conditions to confirm, effect sizes for power, the condition
  list, pilot tuning.
- Exploration may **never** be pooled with confirmation data, or used to select or modify a
  hypothesis already in flight.
- Once a claim is preregistered it is closed to exploration findings. New findings queue for
  the next claim.
- Mode must be distinguishable in every artifact — filename, manifest field, plot watermark.
  If you cannot tell from a file which mode produced it, that file is unusable.

**Determinism.** Counter-based RNG (Philox/Threefry or equivalent) keyed by a content tuple,
never `seed = base + worker_id`, never a global stream consumed in scheduling order. The
requirement is bit-identical results under any core count, batch size, chunking, or
completion order — which per-worker seeding cannot give you, and which will pass every test
you are likely to write before it fails silently in production.

**No silent statistical choices.** Multiplicity correction, CI method, estimator choice and
the allocation rule are preregistered. If code needs one that is not specified, that is a
Tier 3 stop, not a judgment call.

**Novelty is reported, not gated.** Whether the field has already asked the question is a
*graded reported field* obtained from `docs/SEARCH-PROTOCOL.md`, printed next to the claim
the way the comparison type is. It is not a pass/fail condition.

**Every formal object needs a design image.** This repo's papers go to CoG. A result in the
mathematics with no statement a designer could act on is a dynamics result wearing a games
costume, which is the specific rejection both theory documents warn about. The check is
concrete: name the design decision the result changes. If you cannot, say so in the artifact.

---

## 7. Definition of done

Nothing is done because it runs.

| Work type | Done means |
|---|---|
| Any component on `SURFACES.md` | Build memo approved; `DECISIONS.md` entry written; deterministic under seed across core counts; validated against a case where the answer is known independently |
| Estimator | Recovers ground truth on every applicable synthetic case, including the degenerate and null ones, with stated bias and variance |
| Experiment run | Manifest records config, seed, commit, prereg hash, realized conditions, and mode |
| Analysis | Registration hash verified; multiplicity correction applied; CIs reported; comparison type and N stated |
| Literature claim | Read in the original, `[V]` tier, row in `CITATIONS.md` |
| Theory-heavy artifact | Red-team pass run, findings independently verified, outcome recorded in the artifact |
| Any Tier 2+ change | `DECISIONS.md` entry written |
| Any load-bearing choice | `DECISIONS_LEDGER.md` row written, unmarked, no recommendation |

---

## 8. Context budget

Long sessions degrade. Manage it deliberately.

- Read the `DECISIONS.md` index, not the file. Pull entries on demand.
- Read the section of the theory document you need, not the document. `CanvasControl.md` is
  1920 lines; `chaos-games-theory.md` is 578. Neither is a session-start read — `HANDOFF.md`
  tells you which section you need.
- If a session exceeds roughly two hours of work, or you notice you are re-deriving something
  established earlier: **stop, write the handoff, propose a fresh session.** A clean handoff
  beats a degraded continuation. This is a legitimate reason to end early.
- Prefer re-reading a file to reconstructing it from memory of earlier in the session.

---

## 9. Literature

The declared search protocol is `docs/SEARCH-PROTOCOL.md`: fixed terms, fixed venues, fixed
stopping rule, archived per run. Its output is a reported number, not a verdict.

Two standing rules, both from the 2026-08-16 check:

- **`[V]` / `[V-sub]` / `[T]` evidence tiers travel with every retrieval.** A claim assembled
  from `[T]` (tool-extracted, not read in the original) is reported as such and may not carry
  a novelty claim.
- **`CITATIONS.md` §4 is the open-items list.** Before citing anything in a paper-facing
  artifact, check whether it is on it. `O-17` currently blocks a novelty sentence in this
  portfolio; that is what an open item looks like in practice.

---

## 10. Adding a project

`docs/templates/NEW-PROJECT.md` has the checklist. In short: nine files in
`projects/<slug>/`, a row in `docs/PORTFOLIO.md`, a section in `DECISIONS_LEDGER.md` if it
does not have one, and a `SURFACES.md` written before the first line of code — not after.
