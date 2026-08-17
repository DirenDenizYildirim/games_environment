#!/usr/bin/env python3
"""PreToolUse hook — the Tier 3 backstop.

Blocks, with an explanation:
  1. any write to a theory document in ~/MainIdeas/Theories/  (Tier 3, CLAUDE.md §6)
  2. any write to a PREREGISTRATION.md that is no longer marked as a stub

Asks first, with the rules, on:
  3. any write to DECISIONS_LEDGER.md — where the four rules in PROTOCOL.md §5.7
     apply and the mark column must stay empty

This is a backstop, not the rule. The rule is in CLAUDE.md §2 and the tier gate;
a hook that fires means the gate was already walked past.

Exit 2 blocks the call and sends stderr to the model.
"""
import json
import os
import sys

BLOCK = 2
ALLOW = 0


def load_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def main():
    data = load_input()
    tool = data.get("tool_name", "")
    if tool not in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
        return ALLOW

    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path:
        return ALLOW
    real = os.path.realpath(os.path.expanduser(path))
    norm = real.replace("\\", "/")

    # 1 — theory documents are read-only from this repo
    if "/MainIdeas/Theories/" in norm:
        sys.stderr.write(
            "TIER 3 — BLOCKED. Theory documents in ~/MainIdeas/Theories/ are the "
            "authoritative statement of what a project claims, and they are read-only "
            "from this repo (CLAUDE.md §6, PROTOCOL.md §3.1).\n\n"
            "If work here implies a theory document is wrong, that is a FINDING to report "
            "and a DECISIONS_LEDGER.md row to write — not an edit to make. Use /ledger-row.\n\n"
            "If he has explicitly asked for a theory-document edit, he makes it himself, "
            "or disables this hook deliberately for that turn.\n"
        )
        return BLOCK

    # 2 — a preregistration that is no longer a stub is locked
    if os.path.basename(norm) == "PREREGISTRATION.md":
        existing = ""
        try:
            with open(real, encoding="utf-8") as fh:
                existing = fh.read(4000)
        except OSError:
            existing = ""
        if existing and "STUB — NOT LOCKED" not in existing:
            sys.stderr.write(
                "TIER 3 — BLOCKED. This PREREGISTRATION.md no longer carries the "
                "`STUB — NOT LOCKED` banner, so it is being treated as filled in.\n\n"
                "The preregistration is a one-way door (PROTOCOL.md §5.5). After its git tag, "
                "the analysis entrypoint verifies the SHA-256 of these bytes against the tag "
                "and refuses to run on mismatch. Editing it changes that hash.\n\n"
                "Stop and report. If a value in it is genuinely wrong, that is a Tier 3 "
                "decision made in its own commit, by him, never as a side effect of "
                "implementation.\n"
            )
            return BLOCK

    # 3 — the ledger: allowed, but deliberately
    if os.path.basename(norm) == "DECISIONS_LEDGER.md":
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": (
                    "Writing to DECISIONS_LEDGER.md. Four rules (PROTOCOL.md §5.7):\n"
                    "  1. No recommendation — the blast-radius column is factual.\n"
                    "  2. The mark column stays ☐. C / A / ? are his marks; never fill one in.\n"
                    "  3. State it as a choice, not an assumption the reader has to catch.\n"
                    "  4. Findings and bug fixes do not go here — only recommendations and "
                    "invented parameters get logged instead of adopted."
                ),
            }
        }))
        return ALLOW

    return ALLOW


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # a broken guard must not block all work
        sys.stderr.write(f"(tier3-guard hook failed, allowing: {exc})\n")
        sys.exit(0)
