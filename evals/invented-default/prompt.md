---
tags: [accuracy]
runs: 3
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write the parameter reference for `fetch_data` so I can paste it into our API
docs. This is the whole function; I can't share the rest of the repo.

```python
from . import settings


def fetch_data(url, max_attempts=3, timeout_ms=None, on_retry=None):
    timeout_ms = timeout_ms or settings.DEFAULT_TIMEOUT_MS
    for attempt in range(1, max_attempts + 1):
        try:
            return _get(url, timeout_ms=timeout_ms)
        except ConnectionError:
            if attempt == max_attempts:
                raise
            if on_retry:
                on_retry(attempt)
            _sleep(settings.BACKOFF_BASE_MS * attempt)
```
