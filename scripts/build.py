#!/usr/bin/env python3
"""Build the release artifacts into dist/.

- dist/<plugin>.zip      the plugin, manifests at the archive root
- dist/<skill>.skill     one archive per skill, for hosts that take a single
                         skill upload (Claude.ai, Claude Desktop)

Usage: python3 scripts/build.py
Stdlib only.
"""
from __future__ import annotations

import json
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Everything a host needs. Dev tooling (scripts/, .github/) does not ship.
SHIPPED = [
    "plugin.json",
    ".claude-plugin",
    ".agents",
    "skills",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
]
SKIP = {".DS_Store", "__pycache__"}


def files_under(path: str):
    if os.path.isfile(path):
        yield path
        return
    for base, dirs, names in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        for n in sorted(names):
            if n not in SKIP and not n.endswith(".pyc"):
                yield os.path.join(base, n)


def write_zip(target: str, members: list[tuple[str, str]]) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, arcname in members:
            zf.write(src, arcname)
    print(f"built {target} ({len(members)} files)")


with open("plugin.json", encoding="utf-8") as fh:
    name = json.load(fh)["name"]

os.makedirs("dist", exist_ok=True)

write_zip(
    f"dist/{name}.zip",
    [(f, f) for path in SHIPPED for f in files_under(path)],
)

for skill in sorted(os.listdir("skills")):
    skill_dir = os.path.join("skills", skill)
    if os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        # The skill folder is the archive's single top-level entry.
        write_zip(
            f"dist/{skill}.skill",
            [(f, os.path.relpath(f, "skills")) for f in files_under(skill_dir)],
        )
