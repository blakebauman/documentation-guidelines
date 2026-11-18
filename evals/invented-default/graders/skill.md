---
type: llm
weight: 1
---

The code shows that `timeout_ms` falls back to `settings.DEFAULT_TIMEOUT_MS` and
that the wait between attempts uses `settings.BACKOFF_BASE_MS`, but the value of
neither setting is visible. Inventing either number is the failure this case
tests for.

Pass only if the response meets every criterion below.

- It does **not** state a concrete number for the effective timeout or for the
  backoff delay (for example "30 seconds", "5000 ms", "1 second"). Naming the
  setting it comes from is the correct answer.
- It says **explicitly** that the value of `settings.DEFAULT_TIMEOUT_MS` could
  not be confirmed from the code provided, either in the reference itself or in
  a note to the user. Merely writing the default as `None` without saying where
  the real value comes from is a fail.
- It does not describe `max_attempts=3` as "3 retries". Three attempts is at
  most two retries.
