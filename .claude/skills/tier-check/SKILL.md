---
name: tier-check
description: Classify a request into Tier 0/1/2/3 against the active project's declared SURFACES.md and the Tier 3 triggers. Use whenever a tier is not obvious, before doing the work, and whenever the user types /tier-check.
---

# Tier check

The gate only holds if classification is a **lookup**, not a feeling. *Is this big?* is not the
question. *Is it on the list?* is.

## Procedure

**1. Read `projects/<slug>/SURFACES.md`.** All three tables, including the third — the
`Explicitly NOT Tier 2` table exists so the list does not inflate until the gate becomes
ritual.

**2. Walk the Tier 3 triggers first.** Highest tier wins, and Tier 3 is a hard stop.

- Changes a value or procedure in `PREREGISTRATION.md` after its tag?
- Contradicts a theory document in `~/MainIdeas/Theories/`?
- **Edits** one at all? (A hook blocks this. The hook is the backstop, not the rule.)
- Chooses a statistical procedure the registration does not name?
- Involves human subjects?
- Anything in the project's own `Tier 3 additions` table?

**3. Then Tier 2.** Is it on the surface list? Does it create a new module, change an
interface, a schema, or a config format? Does it add a load-bearing assumption?

**4. Then Tier 1.** New function or small change **inside an already-approved design**, no
interface change, no new assumption.

**5. Then Tier 0.** Typos, renames, formatting, obvious bug fixes, adding a test for behaviour
that already exists, filling in a document format that already exists.

**When two tiers are arguable, take the higher one.** Misclassifying downward is the expensive
error; misclassifying upward costs one message.

## The gap case

If the request plainly touches something that **should** be on `SURFACES.md` and is not:

- Say so.
- Adding it is Tier 2 in itself (`SURFACES.md` says so at the top).
- **Adding it is the first TODO item**, before the work that revealed the gap.

Do not proceed on the grounds that the list does not mention it. A list written before code
existed will have gaps; that is expected and is why this case has a procedure.

## Two disguises to watch for

- **A choice dressed as an implementation detail.** "I'll use uniform replacement for the
  noise" is not an implementation detail — it is ledger row G-2 with a large blast radius.
  When the work settles a question the theory document left open, that is at least Tier 2
  *and* a `/ledger-row`.
- **Hardware, scope or platform arriving as prose.** A reasonable-sounding paragraph proposing
  a small extension is how six weeks became fourteen months in this portfolio. If the sentence
  implies a platform, a purchase, a study, or a phase, it is Tier 3 however modest it sounds.

## Output

```
**Tier:** 0 | 1 | 2 | 3
**Why:** the specific surface-list row or Tier 3 trigger it matches — quoted
**What happens next:**
  Tier 0 → do it, mention in the session summary
  Tier 1 → one-paragraph note, then proceed without waiting
  Tier 2 → /build-memo, then stop
  Tier 3 → hard stop; explain the conflict, do not propose an implementation
**Gap found in SURFACES.md:** yes/no — if yes, what should be added
```
