# HANDOFF — canvascurse
_Last session: 2026-08-17 | no repo history yet | scaffolding created_

## Current state

Theory document at v1.4, 1920 lines, three companion documents, twelve milestones. Nine
ledger rows, **none marked**. No code, no preregistration, no cost model. This build
environment was created 2026-08-17 and contains no work product yet.

The theory is in better shape than any other document in the portfolio — red-teamed across
four versions, with its own self-diagnosis kept visible in §1.2. **The problem is size, not
soundness:** roughly 3× over-scoped for 1 March 2027.

Standing portfolio advice as of 2026-08-17 is to **defer this and run `chaos-games` Paper A
as the CoG bet.** That is advice, not a decision, and it is not marked.

## In flight

Nothing. Scaffolding only. `SURFACES.md` is provisional, `PREREGISTRATION.md` is a stub, and
`BUDGET.md` is deliberately empty of numbers because costing it requires the scope cut first.

## Blocked

- **The related-work section**, on **O-7** — hand sweep of CoG/FDG/AIIDE 2019–2025 for
  indirect-control papers, half a day. `SEARCH-PROTOCOL.md` §3 states explicitly that a tool
  sweep does not substitute for this one.
- **`BUDGET.md`**, on the scope decision. Twelve milestones cannot be costed until it is known
  which of them are in the paper.

## Next actions

Ordered. Items 1–3 are pre-September desk work and none needs code.

1. **O-1 — *Lemmings* Builder step duration vs lemming walk speed** (<1 hr). Play it, or read
   NeoLemmix / lix source. It is milestone M−1 and it is the cheapest open item in the
   portfolio.
2. **O-7 — the hand sweep** (half a day). Blocks related work. Archive it under
   `SEARCH-PROTOCOL.md` §6, with the surfaces-not-reached section.
3. **O-8 — robust and tube MPC** (Langson et al.; Majumdar & Tedrake), 1 day. This is
   **threat 17** and milestone M0b. §5.7 needs an explicit delta against tube MPC, and
   without it a control-literate reviewer supplies one.
4. **Cost the twelve milestones** and mark which are mandatory for a single paper. This is
   the input to the scope decision, and producing it is Tier 1 — *making* the cut is his.

## Open questions

All his. All unmarked ledger rows.

- **C-2** — is `Π_ν` (observation noise) a real uncertainty channel or a knob invented to
  rescue the theory? §2.5 says its absence in v1.0 "was fatal." Q-5 asks the hostile version.
  Threat 1 says a reviewer will ask it too. **Every result in §5 rests on this.**
- **C-1** — does v1.4 actually answer §1.2's own diagnosis, or does the drone/beacon
  substitution still go through unchanged?
- **C-7** — one paper or two? Stated in §9 as "two, not one," then not done.
- **C-8** — is the α = 1 vs α = 2 asymptote contrast strong enough to carry the primary
  figure? §7.1 says the hyperbola alone is weak evidence, so if this goes the theoretical
  contribution goes with it.

## Traps for next session

- **v1.4 inverted the precedence.** §4 is the paper; §5 is the method (ledger **C-3**).
  v1.0–v1.3 said the opposite and most of the document's bulk is still §5. A session that
  leads with the mathematics has silently reverted to v1.3.
- **Read §14 before using any symbol.** 1920 lines, dense notation, and `FAILURE-MODES.md`
  F-2 is the failure that costs the most per occurrence.
- **The design document wins on designer-facing questions.** Explicit precedence in the
  theory document's header, and easy to forget when the theory document is the one open.
- **§5.7 already concedes the beam-optics machinery is standard.** Do not re-argue novelty
  there; the novelty claim is the application. Re-arguing it is `FAILURE-MODES.md` F-7.
- **Length is not the drift signal.** This document is the portfolio's proof of that. Do not
  cut it for being long; cut it for being off the two questions in §1.2.
