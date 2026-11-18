---
type: llm
weight: 1
---

The function has exactly one non-obvious idea: it fetches `limit + 1` rows so it
can tell whether another page exists without a second count query, then trims
the extra row. Everything else reads plainly from the code.

Pass only if the response meets every criterion below.

- The code itself is unchanged: same statements, same names, same order. Only
  comments or a docstring were added.
- A comment or the docstring explains **why** `limit + 1` rows are fetched: to
  detect whether there is a next page.
- If a docstring is present, it does not claim behaviour the code does not
  show, such as raising a specific exception, a maximum limit, or a sort
  direction other than ascending `id`.
- The response does not add type hints, rename variables, or restructure the
  function "while it was there".
