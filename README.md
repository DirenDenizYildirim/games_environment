# Games_env

Build environment for two IEEE CoG 2027 papers: **`chaos-games`** and **`canvascurse`**.

**There is no code here, and that is the current correct state.** Code starts September 2026.
What exists now is the operating discipline it will be written under, plus the Claude Code
tooling that enforces it.

```
CLAUDE.md                    auto-loaded every session; short by design
docs/PROTOCOL.md             the full operating protocol
docs/PORTFOLIO.md            projects, calendar, gate state, live tensions
docs/FAILURE-MODES.md        ten recurring mistakes, with detectors
docs/SEARCH-PROTOCOL.md      declared literature search for games venues
docs/templates/              how to add a project
projects/chaos-games/        nine state documents
projects/canvascurse/        nine state documents
.claude/agents/              six — four red-team lenses, a verifier, a sweeper
.claude/skills/              nine slash commands
.claude/workflows/           three — redteam, litsweep, doc-audit
.claude/hooks/               three — session start, Tier 3 guard, handoff guard
tools/protocol-drift.py      drift detector against the sibling environment
```

## The theory lives elsewhere

Both theory documents stay in `~/MainIdeas/Theories/` and are referenced by path:

| Project | Theory document |
|---|---|
| `chaos-games` | `~/MainIdeas/Theories/chaos-games-theory.md` |
| `canvascurse` | `~/MainIdeas/Theories/CanvasControl.md` |

**They are read-only from here.** Editing one is Tier 3 and a hook blocks it. When work here
implies a theory document is wrong, that is a finding to report and a ledger row to write.

**The trade-off:** this repo is not self-contained. Push it to GitHub, move it, or hand it to
someone else and every theory reference breaks. That was the deliberate choice — one copy that
cannot drift, over two that can. If it ever needs to stand alone, vendor the documents in at
that moment and record the vendoring date.

## Start here

```bash
cd ~/Builds/Games_env && claude
```

Then `/session-start`. It reads the active project's `HANDOFF.md`, `SURFACES.md`, the
`DECISIONS.md` index and `RISKS.md`, then produces a tiered TODO list. Tier 2 or 3 in that
list means stop and wait.

## Commands

| Command | What it does |
|---|---|
| `/session-start` | The §2.1 ritual — read state, produce a tiered TODO list |
| `/session-end` | The §2.3 ritual — overwrite HANDOFF, update what earned it |
| `/tier-check` | Classify a request against the project's declared surfaces |
| `/build-memo` | The Tier 2 memo, then stop |
| `/objection` | Structured pushback when a request should not be complied with |
| `/redteam` | The §3.3 adversarial pass — lenses, then independent verification |
| `/litsweep` | The declared pre-emption search, archived |
| `/ledger-row` | Log a load-bearing choice instead of adopting it |
| `/drift-check` | Does this document still answer the question it was created to answer |

## What the hooks do

- **SessionStart** prints a compact orientation block, warns if `~/MainIdeas` cannot be
  reached — which would silently break every theory reference in the repo — and reports
  protocol drift against `Robotics_env`, staying silent when there is none.
- **PreToolUse** blocks writes to `~/MainIdeas/Theories/**` and to a `PREREGISTRATION.md` that
  is no longer marked a stub; asks before writing to `DECISIONS_LEDGER.md`, restating the four
  rules.
- **Stop** refuses to end a session that modified a project without updating that project's
  `HANDOFF.md`. It fires at most once and stays silent on read-only sessions. The session-end
  documents themselves — DIARY, DECISIONS, RISKS, ASSUMPTIONS — do not count as work, because
  §2.3 writes them *after* the handoff and would otherwise trip the guard every time.

Hooks are Python 3, no external dependencies. They fail open — a broken hook never blocks
work.

## The one rule that matters most

**A load-bearing choice gets logged, not adopted.** When a session settles a question the
theory document left open, that becomes a row in
`~/MainIdeas/Supporting_Docs/DECISIONS_LEDGER.md` — unmarked, no recommendation. Everything
else here exists to serve that.
