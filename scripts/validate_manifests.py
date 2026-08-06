#!/usr/bin/env python3
"""Structural checks on the four platform manifests and every local link.

This plugin ships to three agent platforms from one repository, so a version
bumped in one manifest and forgotten in another is the most likely defect, and
a broken relative link in a repository whose whole trust argument is "read it
yourself" is the most expensive one.

Usage: python3 scripts/validate_manifests.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTACT = "build@arrakis.security"

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_json(rel: str) -> dict | None:
    p = ROOT / rel
    if not p.exists():
        fail(f"{rel}: missing")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{rel}: invalid JSON — {e}")
        return None


def main() -> int:
    claude = load_json(".claude-plugin/plugin.json")
    market = load_json(".claude-plugin/marketplace.json")
    codex = load_json(".codex-plugin/plugin.json")
    gemini = load_json("gemini-extension.json")

    # --- one name, one version, everywhere
    versions: dict[str, str] = {}
    names: dict[str, str] = {}

    for label, doc in (("claude", claude), ("codex", codex),
                       ("gemini", gemini)):
        if doc:
            versions[label] = str(doc.get("version"))
            names[label] = str(doc.get("name"))

    if market:
        plugins = market.get("plugins") or []
        if len(plugins) != 1:
            fail(".claude-plugin/marketplace.json: expected exactly one plugin "
                 f"entry, found {len(plugins)}")
        if plugins:
            versions["marketplace"] = str(plugins[0].get("version"))
            names["marketplace"] = str(plugins[0].get("name"))

    if len(set(versions.values())) > 1:
        fail(f"version mismatch across manifests: {versions}")
    if len(set(names.values())) > 1:
        fail(f"plugin name mismatch across manifests: {names}")

    declared = next(iter(versions.values()), None)

    # --- the version the application payload reports must match the manifests
    apply_skill = ROOT / "skills/apply-to-arrakis/SKILL.md"
    if apply_skill.exists() and declared:
        body = apply_skill.read_text(encoding="utf-8")
        for m in re.finditer(r"PLUGIN_VERSION\s*=\s*([0-9][^\s]*)", body):
            if m.group(1) != declared:
                fail(f"skills/apply-to-arrakis/SKILL.md: PLUGIN_VERSION "
                     f"{m.group(1)} != manifest version {declared}")
        for m in re.finditer(r'"plugin_version"\s*:\s*"([^"]+)"', body):
            if m.group(1) != declared:
                fail(f"skills/apply-to-arrakis/SKILL.md: payload "
                     f"plugin_version {m.group(1)} != manifest {declared}")

    # --- contact address consistent wherever it appears in a manifest
    for label, doc in (("claude", claude), ("codex", codex),
                       ("marketplace", market)):
        if not doc:
            continue
        blob = json.dumps(doc)
        for addr in set(re.findall(r"[\w.+-]+@[\w.-]+", blob)):
            if addr != CONTACT:
                fail(f"{label} manifest: unexpected contact address {addr} "
                     f"(expected {CONTACT})")

    # --- manifest file pointers must resolve
    if gemini:
        ctx = gemini.get("contextFileName")
        if ctx and not (ROOT / ctx).exists():
            fail(f"gemini-extension.json: contextFileName {ctx} does not exist")
    if codex:
        skills = codex.get("skills")
        if skills and not (ROOT / skills.strip("./")).is_dir():
            fail(f".codex-plugin/plugin.json: skills path {skills} is not a "
                 f"directory")

    # --- every skill has usable frontmatter
    for skill in sorted(ROOT.glob("skills/*/SKILL.md")):
        head = skill.read_text(encoding="utf-8").split("---")
        if len(head) < 3 or not head[0].strip() == "":
            fail(f"{skill.relative_to(ROOT)}: missing YAML frontmatter")
            continue
        fm = head[1]
        for key in ("name:", "description:"):
            if key not in fm:
                fail(f"{skill.relative_to(ROOT)}: frontmatter missing {key}")
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        if name and name.group(1) != skill.parent.name:
            fail(f"{skill.relative_to(ROOT)}: frontmatter name "
                 f"{name.group(1)} != directory {skill.parent.name}")

    # --- every command file declares a description
    for cmd in sorted(ROOT.glob("commands/*")):
        body = cmd.read_text(encoding="utf-8")
        if "description" not in body:
            fail(f"{cmd.relative_to(ROOT)}: no description declared")

    # --- relative markdown links resolve
    link = re.compile(r"\[[^\]]+\]\((?!https?:|mailto:|#)([^)\s]+)\)")
    for md in sorted(ROOT.rglob("*.md")):
        if ".git/" in str(md):
            continue
        for m in link.finditer(md.read_text(encoding="utf-8")):
            target = (md.parent / m.group(1).split("#")[0]).resolve()
            if not target.exists():
                fail(f"{md.relative_to(ROOT)}: broken link {m.group(1)}")

    if errors:
        print("manifests: FAIL\n")
        for e in errors:
            print(f"  {e}")
        print(f"\n{len(errors)} problem(s).")
        return 1
    print(f"manifests: ok — version {declared} consistent across "
          f"{len(versions)} manifests")
    return 0


if __name__ == "__main__":
    sys.exit(main())
