# AGENTS.md

Guidance for AI coding agents working in this repository.

This repo packages one Agent Skill, `documentation-guidelines`, as a plugin that
several agent runtimes can install. The repo root is the plugin root.

## Layout

- `skills/documentation-guidelines/SKILL.md` — the skill. The only source of its text.
- `plugin.json` — Agent Plugins 1.0 manifest (Codex, Antigravity, and other hosts that read the portable format).
- `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` — Claude Code manifest and marketplace.
- `.agents/plugins/marketplace.json` — Codex marketplace.
- `scripts/`, `.github/` — dev tooling; not included in release artifacts.

## The invariants

`scripts/validate.py` and CI enforce these:

- **One version, three places.** `plugin.json`, `.claude-plugin/plugin.json`, and
  the entry in `.claude-plugin/marketplace.json` must agree. Bump all three.
- **`plugin.json` uses only Agent Plugins fields.** The schema rejects any other
  top-level key. Host-specific settings go under `extensions`.
- **Skill `name` matches its directory name**, and the description is at most
  1024 characters.
- **No `SKILL.md` at the repo root.** Skills live under `skills/`.
- **Stdlib only** in `scripts/`. CI runs on Python 3.10 with no pip step.

Before committing, run:

```bash
python3 scripts/validate.py
```

When the skill or a manifest changes, update `CHANGELOG.md`. When install steps
change, update `README.md`.
