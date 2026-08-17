---
name: drift-check
description: Test whether a document still answers the question it was created to answer, by reading it against its seed in MainIdeas/topics.md. Detects FAILURE-MODES.md F-9 — the silent choice. Use before accepting any large addition to a theory document, and whenever the user types /drift-check.
---

# Drift check

Tests `FAILURE-MODES.md` **F-9**: a document answers a question nobody asked it, and the
answer becomes load-bearing without ever being visible as a choice.

**Size is not the signal.** `CanvasControl.md` is 1920 lines and did not drift.
`Anisotropic Protective Coverage` reached 805 and drifted badly. The difference is that
CanvasControl's §1.2 keeps re-stating the two questions the project started from.

> **A document that keeps saying why it exists does not drift. One that only says what it now
> is, does.**

## Three tests, increasing cost

### 1. The seed test

Open `~/MainIdeas/topics.md` and find the seed this document descends from. There are
four seeds:

| Seed | Subject | Document |
|---|---|---|
| 1 | Kirby Canvas Curse AI — you control the pen | `CanvasControl.md` |
| 2 | Chaotic environments in robotics | `chaos-robotics-theory.md` |
| 3 | Multi-purpose swarms | **none** |
| 4 | Defensive shielding swarms | `APC_Cut.md` |

Then ask: **does the current document still answer that?**

**Three documents have no seed** — `dda-axis`, `TrainerCoaching`, `rain-world-rl` — and
`chaos-games` descends from seed 2 while answering it in a different field entirely (ledger
**X-1b**). *"No matching seed"* is a legitimate result. Report it as a fact, not a defect.

### 2. The choice test

For each load-bearing statement in the addition under review, classify it:

- **Finding** — evidence forced it. Goes straight in.
- **Choice** — a different answer was available and would change downstream work.
  **Becomes a `DECISIONS_LEDGER.md` row, unmarked, no recommendation.** `/ledger-row`.

This is the test that actually prevents drift. The other two detect it after the fact.

### 3. The vocabulary test

Grep the document for terms the seed never used. This is how ledger row X-1b was established
on 2026-08-17:

```bash
grep -ci -E 'robot|swarm|hazard|survival|sensor|environment|JAX|GPU' <theory-doc>
```

`chaos-games-theory.md` returned **zero** — which is how it was found to have answered a
robotics seed in board-game terms. Choose the term list from the *seed's* vocabulary, not the
document's, and report both directions: seed words the document dropped, and document words
the seed never contained.

## Also check

- **Does the document re-state its own purpose anywhere past the opening?** If §1 says why it
  exists and nothing after §1 ever mentions it again, that is the drift precondition, whatever
  the current content says.
- **Does the document contain an unaddressed self-diagnosis?** Grep for *"a reviewer may"*,
  *"worth checking whether"*, *"we concede"*, *"nothing changes"*, *"this is the weakest"*.
  `CanvasControl.md` §1.2's substitution diagnosis survived **four versions**. A confession is
  invisible to a reviewer looking for defects.
- **Scale.** Compare the seed's stated ambition to the current one. Seed 4 said *"probably a
  workshop paper in a smaller conference"*; the document specified a fourteen-month four-phase
  hardware programme. Neither is wrong on its own. The **distance** is the finding.

## Output

```
## Drift check — <document>
**Seed:** topics.md §N, or "none — <why>"
**Still answers it:** yes / partly / no — with the specific divergence
**Vocabulary:** seed terms absent from the doc; doc terms absent from the seed
**Scale:** seed ambition → current ambition
**Unmarked choices found:** each one, and whether a ledger row exists
**Unaddressed self-diagnoses:** quoted, with whether anything acted on them
```

**This produces findings, not edits.** Do not fix drift by rewriting a theory document —
that is Tier 3 and a hook blocks it. Report, and write the ledger rows.
