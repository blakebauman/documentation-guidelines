#!/usr/bin/env python3
"""Validate the plugin's manifests and skills.

Checks the invariants that break installs silently:
- every manifest parses and agrees on name and version
- plugin.json conforms to the Agent Plugins 1.0 schema's field list
- both marketplace files list the plugin with a source that resolves
- every skills/<name>/ has a SKILL.md whose `name` matches the directory,
  with a description inside the Agent Skills length limit

Usage: python3 scripts/validate.py   (exit 0 = ok, 1 = errors)
Stdlib only - CI runs this on Python 3.10 with no pip step.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
# The Agent Plugins schema rejects any other top-level key.
AGENT_PLUGINS_FIELDS = {
    "$schema", "name", "version", "description", "author", "homepage",
    "repository", "license", "keywords", "extensions",
}
AUTHOR_FIELDS = {"name", "email", "url"}
KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_NAME = 64
MAX_SKILL_DESCRIPTION = 1024
MAX_MANIFEST_DESCRIPTION = 500

PORTABLE = "plugin.json"
CLAUDE = ".claude-plugin/plugin.json"
CLAUDE_MARKET = ".claude-plugin/marketplace.json"
CODEX_MARKET = ".agents/plugins/marketplace.json"

errors: list[str] = []


def load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as e:  # missing file or invalid JSON
        errors.append(f"{path}: {e}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path}: top level must be an object")
        return {}
    return data


def frontmatter(path: str) -> dict | None:
    """Parse flat `key: value` frontmatter. No yaml dependency."""
    with open(path, encoding="utf-8") as fh:
        m = re.match(r"^---\n(.*?)\n---", fh.read(), re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).split("\n"):
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            out[km.group(1)] = km.group(2).strip()
    return out


# --- plugin manifests ------------------------------------------------------
portable = load(PORTABLE)
claude = load(CLAUDE)

if portable:
    if portable.get("$schema") != AGENT_PLUGINS_SCHEMA:
        errors.append(f"{PORTABLE}: $schema must be {AGENT_PLUGINS_SCHEMA}")
    for key in sorted(set(portable) - AGENT_PLUGINS_FIELDS):
        errors.append(f"{PORTABLE}: {key!r} is not an Agent Plugins field")
    author = portable.get("author", {})
    if not isinstance(author, dict):
        errors.append(f"{PORTABLE}: author must be an object")
    else:
        for key in sorted(set(author) - AUTHOR_FIELDS):
            errors.append(f"{PORTABLE}: author.{key} is not an Agent Plugins field")

for path, manifest in ((PORTABLE, portable), (CLAUDE, claude)):
    if not manifest:
        continue
    name = manifest.get("name", "")
    if not KEBAB.fullmatch(name) or len(name) > MAX_NAME:
        errors.append(f"{path}: name {name!r} must be kebab-case, at most {MAX_NAME} chars")
    if not manifest.get("version"):
        errors.append(f"{path}: version is missing")
    if len(manifest.get("description", "")) > MAX_MANIFEST_DESCRIPTION:
        errors.append(f"{path}: description is over {MAX_MANIFEST_DESCRIPTION} chars")

name = portable.get("name")
version = portable.get("version")
for key in ("name", "version", "description"):
    if portable and claude and portable.get(key) != claude.get(key):
        errors.append(f"{PORTABLE} and {CLAUDE} disagree on {key}")


# --- marketplaces ----------------------------------------------------------
def marketplace_entry(path: str) -> dict:
    entries = [p for p in load(path).get("plugins", []) if p.get("name") == name]
    if len(entries) != 1:
        errors.append(f"{path}: expected exactly one plugin named {name!r}")
        return {}
    return entries[0]


def check_source(path: str, source: object) -> None:
    if not isinstance(source, str) or not source.startswith("./"):
        errors.append(f"{path}: plugin source must be a path starting with ./")
    elif not os.path.isfile(os.path.join(source, PORTABLE)):
        errors.append(f"{path}: source {source!r} has no {PORTABLE}")


entry = marketplace_entry(CLAUDE_MARKET)
if entry:
    check_source(CLAUDE_MARKET, entry.get("source"))
    if entry.get("version") != version:
        errors.append(f"{CLAUDE_MARKET}: version {entry.get('version')!r} != {version!r}")

entry = marketplace_entry(CODEX_MARKET)
if entry:
    source = entry.get("source", {})
    check_source(CODEX_MARKET, source.get("path") if isinstance(source, dict) else source)
    policy = entry.get("policy", {})
    for key in ("installation", "authentication"):
        if not policy.get(key):
            errors.append(f"{CODEX_MARKET}: policy.{key} is required")
    if not entry.get("category"):
        errors.append(f"{CODEX_MARKET}: category is required")

# --- skills ----------------------------------------------------------------
skills = sorted(d for d in os.listdir("skills") if os.path.isdir(os.path.join("skills", d)))
if not skills:
    errors.append("skills/: no skills found")
for skill in skills:
    path = f"skills/{skill}/SKILL.md"
    if not os.path.isfile(path):
        errors.append(f"{path}: missing")
        continue
    fm = frontmatter(path)
    if fm is None:
        errors.append(f"{path}: no YAML frontmatter")
        continue
    if fm.get("name") != skill:
        errors.append(f"{path}: name {fm.get('name')!r} must match the directory {skill!r}")
    if not KEBAB.fullmatch(skill) or len(skill) > MAX_NAME:
        errors.append(f"{path}: name must be kebab-case, at most {MAX_NAME} chars")
    description = fm.get("description", "")
    if not description:
        errors.append(f"{path}: description is missing")
    elif len(description) > MAX_SKILL_DESCRIPTION:
        errors.append(f"{path}: description is {len(description)} chars, limit {MAX_SKILL_DESCRIPTION}")

if os.path.exists("SKILL.md"):
    errors.append("SKILL.md at the repo root shadows skills/ for some installers; keep skills under skills/")

for e in errors:
    print("ERROR:", e)
if errors:
    sys.exit(1)
print(f"ok: {name} {version}, {len(skills)} skill(s)")
