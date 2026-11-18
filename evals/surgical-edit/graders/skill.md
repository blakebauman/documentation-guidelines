---
type: llm
weight: 1
---

The request is a one-fact change. The port appears in two places: the `curl`
example and the `--port` row of the table. The README is written in a
deliberately casual, lowercase voice. It also contains an unrelated
inconsistency: "Node 16 or newer" under requirements versus "we only test on
Node 18 and 20" under notes.

Pass only if the response meets every criterion below.

- Every heading is unchanged, including its lowercase style (`## getting
  going`, `## knobs`, `## notes`). Renaming, capitalising, or reordering a
  heading is a fail.
- The prose sentences outside the two port values are unchanged word for word.
  Rephrasing, capitalising sentence starts, or "tidying" the casual voice is a
  fail.
- It does **not** change either Node version statement in the README.
- It **tells the user** about the Node 16 versus Node 18/20 inconsistency,
  outside the README, as something noticed but left alone. Saying nothing about
  it is a fail.
