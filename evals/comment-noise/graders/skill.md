---
type: llm
weight: 1
---

The function has exactly one non-obvious idea: it fetches `limit + 1` rows so it
can tell whether another page exists without a second count query, then trims
the extra row. Everything else reads plainly from the code.

Pass only if the response meets every criterion below.

- No comment merely restates the line it sits on. Examples that fail: "build
  the query", "filter by customer", "apply the cursor", "get the rows",
  "truncate to limit", "return the result", "return a dict".
- No comment describes what the code would do in some other situation or
  explains general concepts (what pagination is, what a cursor is) that the
  reader of this function does not need.
