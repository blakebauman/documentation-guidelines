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

- The `curl` example now uses port `9090`.
- The `--port` row of the table now shows `9090`.
- No `8080` remains anywhere in the returned README.
- It adds no new sections, badges, notes, or changelog entries to the README.
