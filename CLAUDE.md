# CLAUDE.md

Operating instructions. Auto-loaded every session — deliberately short.
The full protocol is `docs/PROTOCOL.md`; read a section when a rule here points you there.

## 0. What this repo is

A build environment for **two IEEE CoG 2027 papers**. There is **no code yet** and that is
the current correct state — the first code is scheduled for September 2026 and will be
written under the gate in §2, not before it.

| Project | Question | Theory document (authoritative) |
|---|---|---|
| `chaos-games` | At what action-noise level does a game stop separating strong players from weak ones, and is that predictable from structure? | `~/MainIdeas/Theories/chaos-games-theory.md` |
| `canvascurse` | Can level difficulty be measured agent-free, as a budgeted-actuation quantity `ρ*`? | `~/MainIdeas/Theories/CanvasControl.md` |

Per-project state is in `projects/<slug>/`. Portfolio state — deadlines, gates, what is
blocked on what — is `docs/PORTFOLIO.md`. **Read the project's `HANDOFF.md` before its
theory document**; the handoff tells you which section of a 578- or 1920-line document you
actually need.

**These are games papers.** Both theory documents say so in their own words, and both warn
about the same failure: CoG rejects a dynamics paper wearing a games costume. Every formal
object has to cash out into something a designer can act on. That is not a stylistic
preference here, it is an acceptance criterion — see `docs/PROTOCOL.md` §6.

## 1. Prime directives

1. **Plan before building. Explain before building. Get approval before building.** (§3)
2. **Object when the request is a dead end, underspecified, or statistically invalid.**
   Do not silently comply with a bad instruction. (§4)
3. **Log load-bearing choices; do not adopt them.** A choice a different answer would change
   downstream work becomes a row in `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md`,
   carrying the choice, where it lives, and its blast radius — **and no recommendation**.
   It does not get written into a theory document as settled. This is the rule the rest of
   the repo exists to serve. (§5.7)
4. **Never invent load-bearing method silently.** Guessed noise operator, threshold, skill
   proxy, estimator, correction procedure → say so, mark it `ASSUMPTION:` in the code, and
   add a row to the project's `ASSUMPTIONS.md`.
5. **The preregistration is a one-way door.** Once `projects/<slug>/PREREGISTRATION.md` is
   git-tagged, nothing in it changes for the claims in flight. (§3.1 Tier 3)
6. **Write the session record before the session ends.** `projects/<slug>/HANDOFF.md` every
   session, no exceptions. Other files when they earn it. (§5)
7. **Theory-heavy artifacts get an adversarial pass before acceptance.** The trigger is
   syntactic, not a judgment call — §3.3. Findings are **claims, not verdicts**: verify
   independently before acting on one.

## 2. The work gate — tiers

| Tier | What it covers | Protocol |
|---|---|---|
| **0** | Typos, renames, formatting, obvious bug fixes, adding a test for existing behaviour, filling in a document format that already exists | Just do it. Mention in the session summary. |
| **1** | New function or small change inside an already-approved design; no interface changes; no new assumptions | One-paragraph note of what and why, then **proceed without waiting**. |
| **2** | Anything on the project's declared surface list — `projects/<slug>/SURFACES.md` — plus: new module, interface/schema/config change, anything adding a load-bearing assumption | **Build memo → stop → wait for approval.** Format in `docs/PROTOCOL.md` §3.2. |
| **3** | Anything changing a value or procedure fixed in `PREREGISTRATION.md`; contradicting or **editing** a theory document in `~/MainIdeas/Theories/`; choosing a statistical procedure the registration does not name; anything touching human subjects | **Hard stop.** Do not propose an implementation. Explain the conflict. |

When in doubt between two tiers, take the higher one. Misclassifying downward is the
expensive error.

**Session start:** stop and wait for approval only if the TODO list contains a Tier 2 or
Tier 3 item. Tier 0 and Tier 1 items proceed. Full session protocol: `docs/PROTOCOL.md` §2.

## 3. Document map

| File | Job | Cadence |
|---|---|---|
| `docs/PROTOCOL.md` | Full operating protocol — session, memo, objection, review formats | read on demand |
| `docs/PORTFOLIO.md` | Which projects exist, their venue, deadline, gate state | read at session start |
| `docs/FAILURE-MODES.md` | The recurring mistakes and their detectors | **read before any Tier 2/3 artifact** |
| `docs/SEARCH-PROTOCOL.md` | Declared literature-search protocol for games venues | read before any novelty claim |
| `projects/<slug>/HANDOFF.md` | Current state of the world | read first, overwrite last, every session |
| `projects/<slug>/SURFACES.md` | **This project's Tier 2 surfaces** | read before classifying anything |
| `projects/<slug>/DECISIONS.md` | Why the code is like this | read the index; append Tier 2/3 entries |
| `projects/<slug>/RISKS.md` | What is most likely to kill this, and are we watching | check every session |
| `projects/<slug>/DIARY.md` | Surprises, dead ends, changed beliefs | append only when it earns it |
| `projects/<slug>/ASSUMPTIONS.md` | Ledger mirroring every `ASSUMPTION:` marker | append whenever you guess |
| `projects/<slug>/PREREGISTRATION.md` | Locked hypotheses and analysis plan | Tier 3 |
| `projects/<slug>/BUDGET.md` | Compute and calendar ceiling | read before any design |
| `~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` | Portfolio-wide unmarked choices | append; never mark on his behalf |
| `~/MainIdeas/Supporting_Docs/CITATIONS.md` | Verified bibliography; §4 is the open-items list | read before citing anything |

## 4. Epistemic rules (non-negotiable)

- **Explore/confirm never pool.** Two modes, one simulator core. Exploration may inform
  which conditions to confirm and effect sizes for power; it may never be pooled with
  confirmation data or used to modify a hypothesis in flight. Mode must be recoverable from
  every artifact — filename, manifest field, and plot watermark.
- **Determinism.** Counter-based RNG keyed by `(root_seed, condition_id, match_id)` — never
  per-worker seeding. Results bit-identical under any core count, batch size, or execution
  order. A reproducibility failure is a Tier 2 bug and outranks new work.
- **No silent statistical choices.** Multiplicity correction, CI method, estimator choice
  and any sequential-allocation rule are preregistered. If code needs one that is not
  specified, that is a Tier 3 stop, not a judgment call.
- **Every result carries its comparison type and its N.** No exceptions.
- **Never state a literature fact you have not read in the original.** Every literature
  claim checked on 2026-08-16 that had not been read in the original was wrong. Tool-extracted
  quotes are `[T]` tier and may not carry a novelty claim — `docs/SEARCH-PROTOCOL.md` §4.

## 5. Games-specific standards

- **Every formal object needs a design image.** A result in the mathematics with no
  corresponding statement a designer could act on is probably not worth its page at CoG.
  `CanvasControl.md` builds this in explicitly (§5 result ↔ `CanvasControl_GameDesign.md` §6
  image); apply the same test to `chaos-games`.
- **No ROMs, no shipped commercial assets, no decompilation.** Reproducibility at a games
  venue means a reviewer can run it. `topics.md` already ruled out Kirby ROMs for this
  reason, and the Rain World project died on exactly this (Akupara EULA, `CITATIONS.md` §1.4).
- **Human subjects are Tier 3 and calendar-gated.** Ethics approval is irreversible lead
  time, not a formality. Neither project currently plans a study; if one acquires it, that
  is a Tier 3 stop.
- **Store the estimate, not the decision.** Threshold at δ in analysis. Storing pass/fail
  throws away the sensitivity sweep for no gain.
- **Log the search budget.** MCTS budget is `chaos-games`'s skill ladder (ledger row G-3).
  Unequal budgets across conditions manufacture fake threshold shifts.
- **Tests are for what can be silently wrong**: estimators, statistical procedures, seeding,
  the noise operator. Not glue code.

## 6. Never

- Never write code in the same turn as a Tier 2 build memo.
- Never edit a document in `~/MainIdeas/Theories/` — that is Tier 3, and a hook blocks it.
- Never write a recommendation into `DECISIONS_LEDGER.md`, and never mark a row.
- Never pool `explore` and `confirm` data.
- Never seed per-worker.
- Never state a literature fact sourced only from a tool extract.
- Never end a session without writing the project's `HANDOFF.md`.
- Never pad `DIARY.md` to look productive.
- Never report a result without its comparison type and its N.
