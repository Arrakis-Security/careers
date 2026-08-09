#!/usr/bin/env python3
"""Tree hygiene: this repository is text a person can read in one sitting.

A contributor's pull request should never be able to introduce something a
reviewer cannot read — a binary, a symlink pointing out of the tree, an
executable, a 4000-line file nobody will finish. Those are the shapes a
malicious or careless contribution takes in a prose repository.

Usage: python3 scripts/check_tree.py
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_TOP = {
    ".claude-plugin", ".codex-plugin", ".github", ".gitignore", ".gitattributes",
    "AGENTS.md", "GEMINI.md", "LICENSE", "README.md", "SECURITY.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "commands", "docs",
    "gemini-extension.json", "scripts", "skills", "tests",
}

ALLOWED_SUFFIX = {
    ".md", ".json", ".toml", ".yml", ".yaml", ".py", ".sh", ".txt", "",
}

# Scripts are meant to be run; nothing else needs an executable bit.
ALLOWED_EXECUTABLE = {"scripts"}

MAX_BYTES = 60_000
MAX_LINES = 900

errors: list[str] = []


def tracked() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True,
        check=True).stdout
    return [p for p in out.split("\0") if p]


def main() -> int:
    files = tracked()
    if not files:
        print("tree: no tracked files — is this a git checkout?")
        return 1

    for rel in files:
        p = ROOT / rel
        top = rel.split("/")[0]

        if top not in ALLOWED_TOP:
            errors.append(
                f"{rel}: new top-level entry {top!r} — add it to ALLOWED_TOP in "
                f"scripts/check_tree.py in the same reviewed change, or move the "
                f"file under an existing directory")

        if p.is_symlink():
            errors.append(f"{rel}: symlink — not permitted")
            continue
        if not p.exists():
            errors.append(f"{rel}: tracked but missing from the working tree")
            continue

        if p.suffix not in ALLOWED_SUFFIX:
            errors.append(f"{rel}: unexpected file type {p.suffix!r}")

        data = p.read_bytes()
        if b"\0" in data:
            errors.append(f"{rel}: binary content — this repository is text only")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{rel}: not valid UTF-8")
            continue

        if len(data) > MAX_BYTES:
            errors.append(f"{rel}: {len(data)} bytes exceeds {MAX_BYTES} — split "
                          f"it, or a reviewer will not read it")
        lines = text.splitlines()
        if len(lines) > MAX_LINES:
            errors.append(f"{rel}: {len(lines)} lines exceeds {MAX_LINES}")
        if text and not text.endswith("\n"):
            errors.append(f"{rel}: no trailing newline")
        if "\r\n" in text:
            errors.append(f"{rel}: CRLF line endings")
        for n, line in enumerate(lines, 1):
            if line.rstrip() != line:
                errors.append(f"{rel}:{n}: trailing whitespace")
                break

        executable = os.access(p, os.X_OK)
        if executable and top not in ALLOWED_EXECUTABLE:
            errors.append(f"{rel}: executable bit set outside scripts/")

    if errors:
        print("tree: FAIL\n")
        for e in errors:
            print(f"  {e}")
        print(f"\n{len(errors)} problem(s).")
        return 1
    print(f"tree: ok — {len(files)} tracked text files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
