---
type: llm
weight: 1
---

This is a calibration case. The skill says trivial fixes should just be done,
without the audience questions or the closing summary it asks for on larger
tasks. Over-applying the skill here is the failure. A baseline run is expected
to pass most of these; the case exists to catch a regression, not to show a
gain.

Pass only if the response meets every criterion below.

- The returned line reads `Returns` instead of `Retuns`.
- The returned line reads `haven't` instead of `have'nt`.
- The rest of the line is unchanged: same words, same order, still a one-line
  triple-quoted docstring.
