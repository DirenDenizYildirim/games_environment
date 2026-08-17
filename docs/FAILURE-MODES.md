# FAILURE MODES — recurring mistakes, with detectors

Ten patterns. **F-1…F-8** are inherited from the parent protocol, where a single session
proposed ~20 theory amendments and roughly half did not survive adversarial review; the
failures were not random, each pattern recurred, and each has a cheap detector. Where this
portfolio has produced its own instance of a pattern, that instance is the one shown.

**F-9 and F-10 are this portfolio's own**, and they are the two that matter most here.
Neither is a pattern in prose. F-9 is a pattern in *how documents grow*; F-10 is a pattern in
*what review can and cannot see*. Both were found by looking outside the document.

These are **invisible from the inside**. Nearly every inherited instance was committed by an
author who had just correctly criticised the same pattern in someone else's work. Re-reading
your own draft does not catch them.

Read this before producing a Tier 2/3 artifact. Run the detectors before submitting it.

---

## F-1 — Reaching past the gate

**The pattern.** Producing a fully specified, costed, confident artifact that depends on a
premise the project has explicitly not yet verified. The artifact looks like progress and
reads as authoritative, because the speculation is in the *premise*, not the prose.

**This portfolio's instance.** Ledger row **X-3**: every theory document was written before
any code, literature reading, or feasibility check, and *all of them ended with an
unverified-citation confession*. The 2026-08-16 check was the first external contact any of
them had. The live version of this is `chaos-luck` **C4's novelty sentence**, which is
currently forbidden — not discouraged, forbidden — until **O-17** is read in the original.

**Detector.** For every load-bearing factual claim: *which retrieved source says this, and is
it `[V]` or `[T]`?* If the answer is "I know this," stop. Then check the claim against
`CITATIONS.md` §4 — the open-items list exists so nothing quietly becomes "checked."

---

## F-2 — Using a defined quantity outside its definition

**The pattern.** Borrowing a symbol from the theory and applying it in a regime its defining
equation excludes — predicting how it varies in an argument it does not take, or measuring it
while discarding the predicate it is defined by.

**Detector.** Before using a symbol from a theory document's notation table, **re-read its
defining line.** Check what it minimises over, what it is a function of, and what units it
carries. In the parent session this one action would have caught three separate failures.

Both theory documents in this repo have a notation table for exactly this reason —
`CanvasControl.md` §14, `chaos-games-theory.md` §1. Read the table, not your memory of it.

---

## F-3 — Booking the saving, not the cost

**The pattern.** "Cost: none." "Cost: zero." "Cost: negative." "Purely sequencing."

**This portfolio's instance.** APC's hardware programme: six weeks became fourteen months
without any single step ever being costed as the thing that did it (ledger **A-6**, never
marked). Portfolio-wide, ledger **X-2** is the same shape: seven projects scoped at six to
fourteen months each, all targeting 2027, with roughly six months of calendar — and no
document carries a calendar line.

**Detector.** "Cost: none" is almost always false. Ask specifically: does this cost *compute*,
*schedule*, *claim strength*, or a *never-tuned preregistration commitment*? Any artifact that
proposes something must carry a budget line — a number, against `BUDGET.md`.

---

## F-4 — Committing the error you are correcting

**The pattern.** The document written to fix a class of defect contains a fresh instance of it.

**This portfolio's instance.** `chaos-luck`'s **K1 sweep** — a literature check whose whole
job was to find prior art — asserted that measuring an environment before training *"was not
found."* The second sweep found the question asked in **three separate fields** (empowerment,
transfer-entropy controllability, learnability). A search run to prevent unverified claims
produced one.

**Detector.** After writing a correction, apply the correction's own test to the correction.
It takes one pass. It caught nothing in the parent session because nobody ran it.

---

## F-5 — Inflating a real defect into a false claim

**The pattern.** Find a genuine problem; overstate it into something demonstrably untrue. The
inflated version is what a reviewer attacks, and its refutation buries the real finding. In
the parent session, real *underdetermination* was stated as false *"dimensional incoherence"*;
real *degeneracy* as false *"undefined"*; real *ambiguity* as a false *"exponent error"* —
where the original was in fact correct and tighter.

**Detector.** For each defect claim, write the **weakest** statement that still motivates the
fix. If the weak version motivates it, use the weak version. Strength of language is not
strength of argument, and in the parent session the two were inversely correlated.

---

## F-6 — Unoperationalizable criteria

**The pattern.** Proposing a rule that cannot be discharged by exhibiting anything. Trivially
satisfiable as an objection; unfalsifiable as a defence.

**This portfolio's instance.** `topics.md`'s founding question — *"how far can we push the
chaos"* — with `chaos` undefined. The seed says it outright: *"the idea lives or dies in the
definition of chaos in this project."* It stayed unoperationalizable for a year and became
answerable only when ledger row **CR-1** fixed chaos as coping-channel destruction, at which
point `k` became a number you can sweep.

**Detector.** For any proposed condition: *what artifact discharges it?* A citation, an audit,
a control run, a quoted sentence, a declared comparison type. If no artifact discharges it, it
is not a condition — make it a **reported field** instead of a gate.

---

## F-7 — Rhetorical inflation as a tell

**The pattern.** Superlatives attached to the weakest content in the document.

**This portfolio's instance.** Ledger row **X-5**: the theory documents are written in an
institutional register, not the first-person uncertain voice of `topics.md`. *"Where a doc
says 'this is the contribution' or 'this is the paper,' it is worth checking whether that was
concluded or asserted."* The register is itself the tell — `topics.md` says *"my questions
aren't polished here"* and *"maybe we cant have anything around this questions"*; the
documents built from it say "this is the headline result."

**Detector.** Grep your own draft for *most / strongest / cleanest / decisive / immune /
unattackable / the paper / the contribution*. Each hit is a place to re-check the argument,
not the prose. In the parent session the correlation between superlative and defect was
close to 1.

---

## F-8 — Validation located at the benign point

**The pattern.** A test suite is green because every case is evaluated at a point where the
defect does not bite. Nothing in any individual test looks wrong. The estimator is broken and
the suite is honest about everything except where it looked.

**The parent instance, which is worth carrying.** A rank-inversion **positive control** —
the case whose whole job was to prove the pipeline could detect a true inversion — was sited
at a point where two secant spans were matched, and reported power 0.883. Four lines away in
the same file, a test at a point where the spans were 4 and 1 showed the same estimator
recovering the true inversion at **zero** of three effect sizes. The suite was **167 green
with the defect fully present**, and the proof of the defect was in the same file as the
control that missed it.

**Why it is seductive.** Evaluation points get chosen for convenience, symmetry, or roundness
— the middle of the grid, the smallest indices, the point where the arithmetic checks by
hand. Those are exactly the properties that suppress geometry-dependent defects. The test
author is choosing a point to make the *test* clear, not to make the *estimator* sweat, and
there is no moment while writing it where the two goals visibly conflict.

**Detector.** Two questions, both cheap:

1. For every passing case: *what property of the evaluation point could be causing this to
   pass?* Symmetry, matched spacing, a zero, a round number, the interior. Re-run at a point
   that lacks it.
2. For every **positive control**: it must be sited at the **least** favourable point in its
   domain, not the most convenient one. A positive control at a benign point measures nothing
   — it is a test that the code runs.

**Corollary.** The count of green tests is not evidence about coverage. 167 was compatible
with a 68% error in the headline estimator.

**This repo has no code yet, which is why F-8 is here now.** It is cheap to design the
synthetic cases against this rule and expensive to retrofit them.

---

## F-9 — The silent choice *(this portfolio's own)*

**The pattern.** A document answers a question nobody asked it, and the answer becomes load-
bearing without ever being visible as a choice. Not an error — an *adoption*. Every individual
paragraph is defensible; what is missing is the moment where someone decided.

**The instance.** The APC theory document grew from an eleven-line `topics.md` seed —
*"a ball moving north… if there is a threat on the northwest our swarm needs to position
itself"*, targeted by the seed at *"probably a workshop paper in a smaller conference"* — to
**805 lines and a fourteen-month four-phase hardware programme**. Along the way it adopted
**aerial drones**, a platform contradicting its own §12, which said differential-drive ground
robots. Nobody chose that. It surfaced on 2026-08-16 through an unrelated export-control
check, months later. He named it *"the curse of AI writing my theory doc."*

**Why it is seductive.** Answering is more useful than asking, locally and every time. A
document that keeps saying "this is undecided" reads as weak; a document that decides reads
as finished. The failure is invisible per-paragraph and only visible across the whole
document's distance from its seed.

**Size is not the signal.** `CanvasControl.md` is more than twice APC's length and did **not**
drift, because its §1.2 keeps re-stating the two questions the project started from. *A
document that keeps saying why it exists does not drift; one that only says what it now is,
does.*

**Detector — three, in increasing cost:**

1. **The seed test.** Open `topics.md`, find the seed this work descends from, and ask
   whether the current artifact still answers *that*. `/drift-check` runs this.
2. **The choice test.** For each load-bearing statement: is it a *finding* (evidence forced
   it), or a *choice* (a different answer was available)? Findings go in. **Choices become
   `DECISIONS_LEDGER.md` rows, unmarked, with no recommendation** — `PROTOCOL.md` §5.7.
3. **The vocabulary test.** Grep the artifact for terms the seed never used. `chaos-games`
   contains zero occurrences of *robot*, *swarm*, *hazard*, *survival*, *sensor*,
   *environment*, *JAX* or *GPU* — which is how it was established, on 2026-08-17, that it
   had answered seed 2's question in an entirely different field (ledger **X-1b**).

---

## F-10 — Review substituting for contact *(this portfolio's own)*

**The pattern.** A red-team pass returns clean, and the clean result is read as evidence the
artifact is sound. It is not. It is evidence the artifact is *internally consistent*, which is
a different and much weaker property.

**The instance.** Ledger row **X-4**. Red-teaming is this portfolio's quality mechanism —
changelogs, kill gates, threat tables — and it is genuinely strong. It caught **none** of:
the APC platform contradiction; the Akupara EULA that killed the Rain World project; the ITAR
category; a conflated citation; and `CanvasControl.md`'s own §1.2 self-diagnosis, which
survived **four document versions** unaddressed while sitting in the text the reviewers read.

Every one of those needed **external contact** — reading a source in the original, checking a
licence, running a search, opening a patent.

**Detector.** After any review passes, ask the three questions review structurally cannot
answer:

1. *Which claim here rests on a source nobody has opened?* → that is F-1, and the review
   could not see it.
2. *Which constraint is legal, licensing, ethical, or export-related?* → review does not
   check those. They are also the ones that kill projects outright rather than weakening them.
3. *What does the document say about itself that has not been acted on?* → a self-diagnosis in
   the text is invisible to a reviewer looking for defects, because it is not a defect. It is
   a confession, and confessions do not get flagged.

---

## The meta-pattern

Nearly every inherited failure in **F-1…F-7** was committed by an author who had, in the same
document, correctly identified the same pattern in someone else's work. F-4 and F-6 are that
observation made explicit; it applies to all seven.

**F-8, F-9 and F-10 are the exceptions, and the exceptions are the useful part.** None of them
is catchable by reading more carefully. F-8 surfaced when an estimator was re-run somewhere
else. F-9 surfaced through an unrelated export-control check. F-10 surfaced by auditing what
review had historically missed. So:

- For theory-heavy artifacts, **self-review is not sufficient evidence of correctness** —
  `PROTOCOL.md` §3.3.
- For anything numerical, **review is not sufficient either. Move the evaluation point.**
- For anything that grew, **review is not sufficient either. Go back to the seed.**
- For anything external — a source, a licence, a patent, a regulation — **review is worthless.
  Open the thing.**

**And the corollary, equally load-bearing:** red-team findings are *claims*, not verdicts.
Reviewers were right roughly 85% of the time. What made the process work was independently
recomputing the arithmetic, enumerating the feasible sets, and checking the cost ratios
**before** accepting any finding. Adopting reviewer output on authority replaces one unchecked
source with another, which is the failure review exists to prevent.
