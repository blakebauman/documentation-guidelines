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

- It does not ask the user any question before giving the fix.
- It does not include a multi-part summary with headings or labels such as
  "What changed", "Assumptions", or "How it was verified".
- Apart from the corrected line, the response is at most three sentences.
