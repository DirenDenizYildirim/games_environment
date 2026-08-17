#!/usr/bin/env python3
"""Stop hook — refuse to end a session that changed a project without writing its HANDOFF.

CLAUDE.md §6: never end a session without writing the project's HANDOFF.md.
PROTOCOL.md §2.3 step 1.

Fires when a project directory contains a **work** file that was modified during this
session and is newer than that project's own HANDOFF.md — i.e. work happened and was
not recorded. A read-only session changes nothing and this hook stays silent.

Two things deliberately do not count as work:

  1. **The session-end ritual documents themselves.** PROTOCOL.md §2.3 writes HANDOFF.md
     first (step 1) and DIARY / DECISIONS / RISKS / ASSUMPTIONS after it (steps 2-5), and
     step 4 puts a dated line in RISKS.md every session even when nothing changed. Counting
     those as work made the prescribed order guarantee a false positive on exactly the
     sessions that had followed the protocol, which trains you to ignore the hook.

  2. **Anything not touched since this session started.** A fresh clone or checkout stamps
     every file with the same mtime in arbitrary order; without a session floor that reads
     as "work happened" before any has.

The session floor is written to `.claude/.session-start` by the SessionStart hook. If it is
missing the guard still works — it just cannot separate this session's edits from older ones,
so it falls back to the plain "newer than the handoff" comparison.

Loop-safe: honours `stop_hook_active`, so it fires at most once per stop.
Exit 2 blocks the stop and sends stderr to the model.
"""
import json
import os
import sys

BLOCK = 2
ALLOW = 0
IGNORED_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}

# Written by the session-end ritual (PROTOCOL.md §2.3), not evidence that work happened.
# HANDOFF.md is the file being checked; the other four are written *after* it, by design.
RITUAL_DOCS = {"HANDOFF.md", "DIARY.md", "DECISIONS.md", "RISKS.md", "ASSUMPTIONS.md"}

# Shared work that lives outside projects/ and belongs to every project at once — the
# shared simulator is on both projects' SURFACES.md. Empty until such a directory exists;
# add repo-relative directory names here when it does.
SHARED_WORK_DIRS = ()


def newest_work(root, skip_names=()):
    """Newest mtime under root, ignoring ritual documents and dotfiles."""
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


def session_floor(repo):
    """When this session began, per the SessionStart hook. 0.0 if unknown."""
    try:
        with open(os.path.join(repo, ".claude", ".session-start"), encoding="utf-8") as fh:
            return float(fh.read().strip())
    except (OSError, ValueError):
        return 0.0


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

    floor = session_floor(repo)

    # Shared work counts against every project's handoff.
    shared_newest, shared_path = 0.0, None
    for name in SHARED_WORK_DIRS:
        d = os.path.join(repo, name)
        if os.path.isdir(d):
            m, p = newest_work(d, skip_names=RITUAL_DOCS)
            if m > shared_newest:
                shared_newest, shared_path = m, p

    stale = []
    for slug in sorted(os.listdir(projects)):
        pdir = os.path.join(projects, slug)
        if not os.path.isdir(pdir):
            continue

        newest, newest_path = newest_work(pdir, skip_names=RITUAL_DOCS)
        if shared_newest > newest:
            newest, newest_path = shared_newest, shared_path

        # Nothing touched this session — nothing to record.
        if newest <= floor:
            continue

        handoff = os.path.join(pdir, "HANDOFF.md")
        if not os.path.isfile(handoff):
            stale.append((slug, "HANDOFF.md does not exist"))
            continue
        if newest > os.path.getmtime(handoff):
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
