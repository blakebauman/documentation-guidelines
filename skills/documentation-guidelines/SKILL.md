---
name: documentation-guidelines
description: Behavioral guardrails that prevent the most common LLM documentation mistakes — padded or generic prose, invented APIs and defaults, comments that restate code, rewriting docs nobody asked to change, and examples that were never run. Use this skill for ANY task that writes, edits, reviews, or updates documentation, including READMEs, API references, docstrings, code comments, how-to guides, runbooks, changelogs, release notes, PR descriptions, architecture docs, and onboarding pages, even when the user just says "document this," "add comments," or "update the README." It applies alongside format-specific skills (docx, markdown, wiki tools), not instead of them.
license: MIT
---

# Documentation Guidelines

Behavioral guidelines to reduce common LLM documentation mistakes.

The failure modes are consistent: models write for no one in particular, describe behavior they never checked, pad every page with filler, rewrite whole documents to change one line, and ship examples that don't run. Each section below targets one of those habits and explains why it matters, so you can apply the intent rather than the letter.

## Calibrating to the task

These guidelines bias toward accuracy over speed. Scale them to the stakes:

- **Trivial** (typo, broken link, one-line comment): just do it. Still check the fix is correct.
- **Normal** (a README section, docstrings for a module, a how-to): apply all sections briefly.
- **High-stakes** (public API reference, security or compliance docs, runbooks used during incidents, migration guides): apply everything in full, and confirm scope and audience before writing.

## 1. Know the Reader First

**Every document has one primary reader and one job. Decide both before writing.**

Docs written for "everyone" serve no one: beginners get lost and experts wade through basics.

Before writing, settle:
- **Who reads it?** New user, integrating developer, maintainer, operator on call, executive skimming.
- **What kind of doc is it?** Pick one and don't mix them in a single section:
  - *Tutorial* — learning by doing, for newcomers.
  - *How-to* — steps to accomplish a specific goal.
  - *Reference* — complete, exact facts to look up (parameters, flags, return values).
  - *Explanation* — the why: design, tradeoffs, background.
- **What should they be able to do afterward?** If you can't state it in one sentence, the scope is unclear.

**When to ask vs. proceed.** Ask when the audience or doc type is genuinely ambiguous *and* guessing wrong means rewriting the whole thing. Otherwise, infer from context (repo, existing docs, the request), state your choice in one line, and proceed. In unattended runs, always proceed and note the assumption in your summary.

## 2. Accuracy Over Plausibility

**Document only what you verified. Never fill gaps with what "probably" happens.**

A confident, wrong doc is worse than a missing one: readers trust it, act on it, and lose hours.

- Derive behavior from the source — code, config, schemas, tests, CLI `--help` — not from what similar tools usually do.
- Never invent parameters, flags, defaults, environment variables, error messages, version numbers, URLs, or limits.
- If you can't confirm something, say so plainly in the doc ("Default not confirmed — check `config.py`") or flag it in your summary. Don't paper over it.
- Use the exact names the code uses — same casing, same spelling, same units.
- When docs and code disagree, the code is the truth for current behavior. Report the mismatch; don't silently "fix" either one unless asked.

## 3. Say It Once, Plainly

**Shortest text that fully serves the reader. No filler.**

Every sentence costs reading time. Padding buries the one line the reader came for.

- Cut throat-clearing ("In this section, we will explore…"), hype ("powerful," "seamless," "robust"), and closing recaps that repeat what was just said.
- Lead with what the reader needs most: what it does, how to use it, then details and edge cases.
- Prefer concrete over abstract: a real command, a real value, a real error message.
- Use formatting to aid scanning, not to decorate. Headers for navigation, code blocks for anything copyable, tables for genuinely tabular facts. No emoji, no bolding every other phrase, no bullets where a sentence reads better.

**Comments and docstrings explain *why*, not *what*.** The code already says what it does. A comment earns its place by covering intent, a non-obvious constraint, a workaround and its reason, or a gotcha. Delete or don't write comments like `# increment counter`.

## 4. Surgical Edits

**Change only what the request requires. Preserve the document's voice.**

Rewriting a doc to change one fact makes the real change impossible to review and discards the existing authors' decisions.

When editing existing docs:
- Match the existing voice, tense, heading style, terminology, and formatting conventions, even if you'd choose differently.
- Don't restructure, re-headline, or "modernize" sections the request didn't touch.
- When code changes, update every place that describes the changed behavior — and only those places. Search for the old name, flag, or value across the docs so nothing goes stale.

**Mention, don't fix.** If you notice unrelated problems — outdated sections, broken links, contradictions — list them in your summary. The exception: if adjacent text is wrong in a way that would make your change misleading, fix the minimum and call it out.

The test: every changed line should trace directly to the request.

## 5. Verify Before Claiming Done

**A doc isn't done until a reader could follow it and succeed.**

Untested examples are the single most common way docs break trust.

- **Run the examples** — commands, code snippets, API calls — when you have an environment that allows it. Show the actual output, not imagined output.
- If you can't run something, say so in your summary and mark the example as unverified for the user.
- **Check references**: links resolve, file paths exist, referenced functions and sections exist under those names.
- **Walk the steps** as the target reader: is any prerequisite, permission, install step, or config value assumed but never stated?
- **Never** describe output, screenshots, or results you didn't actually observe.

## When reviewing documentation

Apply the same lens to someone else's draft:
- Is the audience and doc type clear and consistent?
- Is every factual claim traceable to the code or a source? Flag anything that looks invented or stale.
- Do the examples run? Are prerequisites stated?
- What could be cut without the reader losing anything?
- Separate "must fix" (wrong, misleading, missing steps) from "optional" (style, wording) so the author knows what blocks publishing.

## Finishing: report honestly

End every non-trivial documentation task with a short summary:
- **What changed** and where.
- **Assumptions** about audience, scope, or behavior.
- **How it was verified** — which examples ran, which links were checked — and, plainly, anything you could *not* verify.
- **Noticed but didn't touch** — stale sections, doc/code mismatches, broken links elsewhere.

Never say a doc is "accurate" or "complete" for something you didn't check against the source.

## Example

Request: "Document the `retry` option in `fetch_data`."

Overbuilt (avoid): a new "Advanced Configuration" chapter, an introduction to the concept of retries, an invented `retry_backoff` parameter "for fine-tuning," a rewrite of the surrounding README in a new voice, and a sample output that was never produced.

Right-sized, added to the existing parameter table in the existing style:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `retry` | `int` | `3` | Times to retry on connection errors. Timeouts are not retried. |

Summary notes: "Default and timeout behavior confirmed in `client.py` lines 40–58. Couldn't run the example (no network in this environment) — marked unverified. Noticed the `timeout` row says seconds but the code uses milliseconds — left as is, please confirm."
