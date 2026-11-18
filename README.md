# Documentation Guidelines

An Agent Skill that stops the most common LLM documentation mistakes: prose
written for no one in particular, invented APIs and defaults, comments that
restate the code, whole-document rewrites to change one line, and examples that
were never run.

The skill is one Markdown file,
[skills/documentation-guidelines/SKILL.md](skills/documentation-guidelines/SKILL.md).
It has no scripts, hooks, or dependencies, so it behaves the same in every
runtime that reads [Agent Skills](https://agentskills.io). The agent loads it
when a task writes, edits, or reviews documentation.

## What it covers

| Section | Rule |
| :-- | :-- |
| Know the reader first | One primary reader and one doc type per document, decided before writing |
| Accuracy over plausibility | Document only what was verified against code, config, or `--help` |
| Say it once, plainly | No filler, no hype; comments explain why, not what |
| Surgical edits | Change only what the request requires; keep the existing voice |
| Verify before claiming done | Run the examples, check the links, walk the steps |
| Report honestly | End with what changed, what was assumed, and what could not be verified |

## Install

Pick your runtime. Each method installs the same skill.

### Claude Code

```
/plugin marketplace add blakebauman/documentation-guidelines
/plugin install documentation-guidelines@documentation-guidelines
```

To update:

```
/plugin marketplace update documentation-guidelines
/reload-plugins
```

### Codex

```bash
codex plugin marketplace add blakebauman/documentation-guidelines
codex plugin add documentation-guidelines@documentation-guidelines
```

To update, run `codex plugin marketplace upgrade documentation-guidelines`.

### Any agent, with the `skills` CLI

The [`skills`](https://github.com/vercel-labs/skills) CLI copies the skill into
the skills directory of the agent you choose, including Cursor, OpenCode,
GitHub Copilot, and Codex:

```bash
npx skills add blakebauman/documentation-guidelines
```

Add `-g` to install for every project instead of the current one, and
`-a <agent>` to target one agent, for example `-a cursor`.

### Antigravity CLI

```bash
agy plugin install https://github.com/blakebauman/documentation-guidelines
```

### VS Code (GitHub Copilot)

Run **Chat: Install Plugin from Source** from the Command Palette and enter
`https://github.com/blakebauman/documentation-guidelines`.

### Claude.ai and Claude Desktop

Download `documentation-guidelines.skill` from the
[latest release](https://github.com/blakebauman/documentation-guidelines/releases/latest)
and upload it in the Skills settings.

### Vertex AI and other ADK agents

Agents built with Google's [Agent Development Kit](https://adk.dev/skills/)
load the skill folder directly. ADK for Python supports skills from v1.25.0.
Copy `skills/documentation-guidelines/` next to your agent source, then:

```python
import pathlib

from google.adk import Agent
from google.adk.skills import load_skill_from_dir
from google.adk.tools import skill_toolset

skill_dir = pathlib.Path(__file__).parent / "skills" / "documentation-guidelines"
toolset = skill_toolset.SkillToolset(skills=[load_skill_from_dir(skill_dir)])

root_agent = Agent(
    model="gemini-flash-latest",
    name="docs_agent",
    instruction="You write and review documentation.",
    tools=[toolset],
)
```

The `skills/` folder must be part of the source you deploy, so that the path
resolves at runtime.

### Manual copy

Copy the `skills/documentation-guidelines/` folder into the skills directory
your agent reads, for example `~/.claude/skills/` or `.agents/skills/`. Keep
the folder name: several runtimes require it to match the `name` in `SKILL.md`.

### What has been tested

| Method | Status |
| :-- | :-- |
| Claude Code | Manifests pass `claude plugin validate` on 2.1.327. Install not run end to end. |
| Codex | Installed from a local checkout with Codex CLI 0.169.1; the skill appears in the session's skill list. |
| `skills` CLI, Antigravity, VS Code, ADK | Written from each vendor's documentation. Not run. |

## Repository layout

```
plugin.json                          Agent Plugins 1.0 manifest
.claude-plugin/plugin.json           Claude Code manifest
.claude-plugin/marketplace.json      Claude Code marketplace
.agents/plugins/marketplace.json     Codex marketplace
skills/documentation-guidelines/     the skill
scripts/validate.py                  checks the manifests and skills agree
scripts/build.py                     builds the release artifacts into dist/
```

## Development

```bash
python3 scripts/validate.py   # run before committing
python3 scripts/build.py      # writes dist/*.zip and dist/*.skill
```

Both scripts need Python 3.10 or later and nothing else. Pushing a `v*` tag that
matches the version in `plugin.json` publishes both artifacts to a GitHub
Release. [AGENTS.md](AGENTS.md) lists the rules the validator enforces.

## License

MIT
