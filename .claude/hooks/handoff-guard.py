#!/usr/bin/env python3
"""Stop hook — refuse to end a session that changed a project without writing its HANDOFF.

CLAUDE.md §6: never end a session without writing the project's HANDOFF.md.
PROTOCOL.md §2.3 step 1.

Fires only when a project directory contains a file modified more recently than
that project's own HANDOFF.md — i.e. work happened and was not recorded. A
read-only session changes nothing and this hook stays silent.

Loop-safe: honours `stop_hook_active`, so it fires at most once per stop.
Exit 2 blocks the stop and sends stderr to the model.
"""
import json
import os
import sys

BLOCK = 2
ALLOW = 0
IGNORED_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def newest_mtime(root, skip_names=()):
    newest = 0.0
    newest_path = None
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]
        for fn in filenames:
            if fn in skip_names or fn.startswith("."):
                continue
            p = os.path.join(dirpath, fn)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if m > newest:
                newest, newest_path = m, p
    return newest, newest_path


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    # Already fired once for this stop — let the session end.
    if data.get("stop_hook_active"):
        return ALLOW

    repo = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    projects = os.path.join(repo, "projects")
    if not os.path.isdir(projects):
        return ALLOW

    stale = []
    for slug in sorted(os.listdir(projects)):
        pdir = os.path.join(projects, slug)
        if not os.path.isdir(pdir):
            continue
        handoff = os.path.join(pdir, "HANDOFF.md")
        if not os.path.isfile(handoff):
            stale.append((slug, "HANDOFF.md does not exist"))
            continue
        h_mtime = os.path.getmtime(handoff)
        newest, newest_path = newest_mtime(pdir, skip_names={"HANDOFF.md"})
        if newest > h_mtime:
            rel = os.path.relpath(newest_path, repo) if newest_path else "?"
            stale.append((slug, f"`{rel}` is newer than its HANDOFF.md"))

    if not stale:
        return ALLOW

    lines = [
        "HANDOFF NOT WRITTEN. This session changed project files without updating the "
        "handoff for those projects:",
        "",
    ]
    for slug, why in stale:
        lines.append(f"  - {slug}: {why}")
    lines += [
        "",
        "PROTOCOL.md §2.3: HANDOFF.md is overwritten every session, no exceptions. State, "
        "not history, under one page.",
        "",
        "Run `/session-end` — it also covers DIARY (only if it earned an entry), DECISIONS "
        "(Tier 2/3 only), RISKS (changes, or a dated line saying nothing changed), "
        "ASSUMPTIONS (every new marker), and DECISIONS_LEDGER (every load-bearing choice "
        "this session surfaced).",
        "",
        "The two fields that matter: `In flight` — precisely where the half-done thing "
        "stops — and `Traps for next session` — anything that cost you fifteen minutes to "
        "discover.",
    ]
    sys.stderr.write("\n".join(lines) + "\n")
    return BLOCK


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never trap a session inside a broken hook
        sys.stderr.write(f"(handoff-guard hook failed, allowing stop: {exc})\n")
        sys.exit(0)
