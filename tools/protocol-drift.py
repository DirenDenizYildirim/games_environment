#!/usr/bin/env python3
"""Detect protocol drift between the two build environments.

`README.md` argues that theory documents are referenced and never copied, because one copy
that cannot drift beats two that can. The operating protocol is the deliberate exception:
`Games_env` and `Robotics_env` each carry their own copy, because `.claude/` tooling and
`CLAUDE.md` only load when the repo is the working directory. That trade owes a detector,
and this is it — every other invariant in these repos has one.

Two sets, checked differently:

  IDENTICAL — must be byte-identical in both repos. Any difference is drift.

  DIVERGENT — expected to differ, because they carry domain-specific content. What is
              checked is not that they match, but that the difference is still the one
              that was last reviewed: the SHA-256 of the unified diff is recorded in
              `tools/protocol-drift.json` and compared against. Editing either copy
              changes the hash, you re-read the diff once, and record it with --update.

The point of the second set is that a *deliberate* edit to one repo's PROTOCOL.md is
invisible today. This makes it announce itself exactly once.

    python3 tools/protocol-drift.py            # check; run from either repo
    python3 tools/protocol-drift.py --quiet    # one line, for the SessionStart hook
    python3 tools/protocol-drift.py --update   # record the current diffs as reviewed

Exit 0 when clean, or when no sibling environment is present (a repo on its own machine
cannot drift against anything). Exit 1 when something moved.
"""
import argparse
import difflib
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(REPO)
BASELINE = os.path.join("tools", "protocol-drift.json")

# Byte-identical in every environment. The three hooks, the four domain-neutral red-team
# agents, the verifier, the skills with no domain content, the settings, this checker and
# its own baseline.
IDENTICAL = [
    ".claude/agents/finding-verifier.md",
    ".claude/agents/redteam-consistency.md",
    ".claude/agents/redteam-quantitative.md",
    ".claude/agents/redteam-technical.md",
    ".claude/hooks/handoff-guard.py",
    ".claude/hooks/session-start.py",
    ".claude/hooks/tier3-guard.py",
    ".claude/settings.json",
    ".claude/skills/build-memo/SKILL.md",
    ".claude/skills/drift-check/SKILL.md",
    ".claude/skills/ledger-row/SKILL.md",
    ".claude/skills/objection/SKILL.md",
    ".claude/skills/session-end/SKILL.md",
    "docs/templates/NEW-PROJECT.md",
    "tools/protocol-drift.py",
    BASELINE.replace(os.sep, "/"),
]

# Expected to differ. The diff itself is what gets version-checked.
DIVERGENT = [
    ".claude/agents/lit-sweeper.md",
    ".claude/skills/litsweep/SKILL.md",
    ".claude/skills/redteam/SKILL.md",
    ".claude/skills/session-start/SKILL.md",
    ".claude/skills/tier-check/SKILL.md",
    ".claude/workflows/doc-audit.js",
    ".claude/workflows/litsweep.js",
    ".claude/workflows/redteam.js",
    ".gitignore",
    "CLAUDE.md",
    "README.md",
    "docs/FAILURE-MODES.md",
    "docs/PORTFOLIO.md",
    "docs/PROTOCOL.md",
    "docs/SEARCH-PROTOCOL.md",
]

# Exists in one environment only, on purpose — the fourth red-team lens differs by domain.
REPO_SPECIFIC = {
    ".claude/agents/redteam-designer.md",
    ".claude/agents/redteam-platform.md",
    ".claude/settings.local.json",
}

# Everything outside these is project state, which is meant to be unrelated between repos.
SHARED_AREAS = (".claude", "docs", "tools")
SHARED_ROOT_FILES = ("CLAUDE.md", "README.md", ".gitignore")
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def is_env(path):
    return os.path.isfile(os.path.join(path, "docs", "PROTOCOL.md")) and os.path.isdir(
        os.path.join(path, ".claude")
    )


def find_envs():
    """Every build environment beside this one, self included, in a stable order."""
    try:
        names = sorted(os.listdir(PARENT))
    except OSError:
        return [REPO]
    envs = [os.path.join(PARENT, n) for n in names if is_env(os.path.join(PARENT, n))]
    return envs or [REPO]


def read_text(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def shared_files(root):
    """Every file in the shared area of one environment, repo-relative, posix separators."""
    found = set()
    for name in SHARED_ROOT_FILES:
        if os.path.isfile(os.path.join(root, name)):
            found.add(name)
    for area in SHARED_AREAS:
        base = os.path.join(root, area)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                found.add(rel.replace(os.sep, "/"))
    return found


def diff_text(a_root, b_root, rel):
    a, b = read_text(os.path.join(a_root, rel)), read_text(os.path.join(b_root, rel))
    if a is None or b is None:
        return None
    return "\n".join(
        difflib.unified_diff(
            a.splitlines(),
            b.splitlines(),
            fromfile=f"{os.path.basename(a_root)}/{rel}",
            tofile=f"{os.path.basename(b_root)}/{rel}",
            lineterm="",
        )
    )


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_baseline():
    data = read_text(os.path.join(REPO, BASELINE))
    if not data:
        return {}
    try:
        return json.loads(data).get("diffs", {})
    except ValueError:
        return {}


def check(a_root, b_root, baseline):
    """Returns (hard, soft, notes) — hard blocks, soft wants a re-read, notes are context."""
    hard, soft, notes = [], [], []
    a_name, b_name = os.path.basename(a_root), os.path.basename(b_root)

    for rel in IDENTICAL:
        a, b = read_text(os.path.join(a_root, rel)), read_text(os.path.join(b_root, rel))
        if a is None or b is None:
            missing = a_name if a is None else b_name
            hard.append(f"{rel} — declared identical but missing from {missing}")
        elif a != b:
            d = diff_text(a_root, b_root, rel) or ""
            n = len([ln for ln in d.splitlines() if ln[:1] in "+-" and ln[:3] not in ("+++", "---")])
            hard.append(f"{rel} — declared identical, differs by {n} line(s)")

    for rel in DIVERGENT:
        d = diff_text(a_root, b_root, rel)
        if d is None:
            hard.append(f"{rel} — declared shared but missing from one environment")
            continue
        if not d.strip():
            notes.append(f"{rel} — declared divergent but now identical")
            continue
        current, recorded = sha(d), baseline.get(rel)
        if recorded is None:
            soft.append(f"{rel} — no reviewed baseline recorded")
        elif current != recorded:
            soft.append(f"{rel} — diff changed since last review ({recorded} → {current})")

    declared = set(IDENTICAL) | set(DIVERGENT) | REPO_SPECIFIC
    for root, other, name in ((a_root, b_root, a_name), (b_root, a_root, b_name)):
        for rel in sorted(shared_files(root) - declared):
            if rel.endswith(".session-start"):
                continue
            where = "both" if os.path.exists(os.path.join(other, rel)) else name
            hard.append(f"{rel} — shared file in {where}, not declared in protocol-drift.py")

    return hard, soft, notes


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--quiet", action="store_true", help="one summary line, for the hook")
    ap.add_argument("--update", action="store_true", help="record current diffs as reviewed")
    args = ap.parse_args()

    envs = find_envs()
    if len(envs) < 2:
        if not args.quiet:
            print("Only one build environment found — nothing to drift against.")
        return 0
    a_root, b_root = envs[0], envs[1]

    if args.update:
        diffs = {}
        for rel in DIVERGENT:
            d = diff_text(a_root, b_root, rel)
            if d and d.strip():
                diffs[rel] = sha(d)
        payload = {
            "_comment": (
                "SHA-256 prefixes of the unified diff between the two environments, for files "
                "that are meant to differ. A changed hash means one copy moved: re-read the "
                "diff, then re-record it with `python3 tools/protocol-drift.py --update`."
            ),
            "pair": [os.path.basename(a_root), os.path.basename(b_root)],
            "diffs": dict(sorted(diffs.items())),
        }
        body = json.dumps(payload, indent=2) + "\n"
        for env in envs:
            path = os.path.join(env, BASELINE)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
        print(f"Recorded {len(diffs)} reviewed diffs into {len(envs)} environment(s).")
        return 0

    hard, soft, notes = check(a_root, b_root, load_baseline())

    if args.quiet:
        if hard or soft:
            bits = []
            if hard:
                bits.append(f"{len(hard)} file(s) that must match do not")
            if soft:
                bits.append(f"{len(soft)} reviewed diff(s) changed")
            print("; ".join(bits) + ".")
            return 1
        return 0

    print(f"Protocol drift: {os.path.basename(a_root)} vs {os.path.basename(b_root)}")
    print()
    for label, rows in (("MUST MATCH — drift", hard), ("REVIEWED DIFF CHANGED", soft), ("NOTE", notes)):
        if rows:
            print(f"{label}:")
            for r in rows:
                print(f"  - {r}")
            print()
    if not (hard or soft or notes):
        print(f"Clean. {len(IDENTICAL)} identical, {len(DIVERGENT)} divergent as recorded.")
        return 0
    if hard or soft:
        print("Inspect with:  diff -u <env-a>/<file> <env-b>/<file>")
        print("Once reviewed: python3 tools/protocol-drift.py --update")
    return 1 if (hard or soft) else 0


if __name__ == "__main__":
    sys.exit(main())
