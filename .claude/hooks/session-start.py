#!/usr/bin/env python3
"""SessionStart hook — print a compact orientation block into context.

Deliberately short. This is not a substitute for /session-start; it is the
thing that reminds you to run it, plus the two or three facts that decide
whether the session should start at all.

Also stamps `.claude/.session-start` with the current time. The Stop hook reads it to
tell this session's edits from older ones — see handoff-guard.py.

stdout is added to the session context. Keep it under ~25 lines.
"""
import os
import re
import subprocess
import sys
import time

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


def read(path, limit=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read(limit) if limit else fh.read()
    except OSError:
        return ""


def stamp_session():
    """Record when this session began, for the Stop hook. Best effort."""
    try:
        with open(os.path.join(REPO, ".claude", ".session-start"), "w", encoding="utf-8") as fh:
            fh.write(str(time.time()))
    except OSError:
        pass


def protocol_drift():
    """One-line drift summary from tools/protocol-drift.py, or None. Silent when clean."""
    checker = os.path.join(REPO, "tools", "protocol-drift.py")
    if not os.path.isfile(checker):
        return None
    try:
        res = subprocess.run(
            [sys.executable or "python3", checker, "--quiet"],
            capture_output=True, text=True, timeout=10,
        )
    except Exception:
        return None
    if res.returncode == 1 and res.stdout.strip():
        return res.stdout.strip().splitlines()[0]
    return None


def main():
    stamp_session()

    out = []
    name = os.path.basename(REPO.rstrip("/"))
    out.append(f"## {name} — no code by design; docs and protocol only")

    projects_dir = os.path.join(REPO, "projects")
    slugs = sorted(
        d for d in os.listdir(projects_dir)
        if os.path.isdir(os.path.join(projects_dir, d))
    ) if os.path.isdir(projects_dir) else []

    if slugs:
        out.append("")
        out.append("**Projects** (state in `projects/<slug>/HANDOFF.md`):")
        for slug in slugs:
            handoff = os.path.join(projects_dir, slug, "HANDOFF.md")
            body = read(handoff)
            note = ""
            if re.search(r"^## Current state\s*\n+\s*\**DEFERRED", body, re.M):
                note = " — DEFERRED"
            else:
                m = re.search(r"^## Blocked\s*\n(.+?)(?=\n## |\Z)", body, re.S | re.M)
                if m:
                    first = next(
                        (ln.strip(" -*_") for ln in m.group(1).splitlines() if ln.strip()),
                        "",
                    )
                    first = re.sub(r"[*_`]", "", first).strip()
                    if first and not first.lower().startswith("nothing"):
                        note = f" — blocked: {first[:88]}"
                    elif first:
                        note = " — not blocked"
            out.append(f"- `{slug}`{note}")

    # Theory documents live outside this repo and are read-only from here.
    theories = os.path.expanduser("~/MainIdeas/Theories")
    if not os.path.isdir(theories):
        out.append("")
        out.append(
            f"**WARNING:** `{theories}` not found. Every theory reference in this repo points "
            "outside it; if MainIdeas moved, they are all broken."
        )

    drift = protocol_drift()
    if drift:
        out.append("")
        out.append(f"**PROTOCOL DRIFT:** {drift}")
        out.append("Run `python3 tools/protocol-drift.py` for the detail.")

    try:
        st = subprocess.run(
            ["git", "-C", REPO, "status", "--porcelain"],
            capture_output=True, text=True, timeout=5,
        )
        if st.returncode == 0:
            dirty = len([ln for ln in st.stdout.splitlines() if ln.strip()])
            out.append("")
            out.append(f"Working tree: {'clean' if dirty == 0 else f'{dirty} uncommitted change(s)'}")
        else:
            out.append("")
            out.append("Not a git repository yet — it should be one before any code exists.")
    except Exception:
        pass

    out.append("")
    out.append(
        "**Start with `/session-start`.** It reads HANDOFF, SURFACES, the DECISIONS index "
        "and RISKS, then produces a tiered TODO list. Tier 2 or 3 in the list means stop "
        "and wait. Do not read a theory document until the handoff tells you which section."
    )
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never break a session on a hook fault
        print(f"(session-start hook failed: {exc})", file=sys.stderr)
        sys.exit(0)
