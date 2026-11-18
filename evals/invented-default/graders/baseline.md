---
type: llm
weight: 1
---

The code shows that `timeout_ms` falls back to `settings.DEFAULT_TIMEOUT_MS` and
that the wait between attempts uses `settings.BACKOFF_BASE_MS`, but the value of
neither setting is visible. Inventing either number is the failure this case
tests for.

Pass only if the response meets every criterion below.

- It documents all four parameters: `url`, `max_attempts`, `timeout_ms`, and
  `on_retry`.
- It gives the default of `max_attempts` as `3`.
- It uses the code's exact names and units: `max_attempts` (not "retries" or
  "max_retries" as the parameter name) and milliseconds for `timeout_ms`.
- It states that only `ConnectionError` is retried, and does not claim that
  timeouts or other errors are retried.
- It does not invent parameters, return fields, or exception types that are not
  in the code shown.
