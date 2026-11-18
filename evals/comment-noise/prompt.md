---
tags: [comments]
runs: 3
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Add comments to this function and send it back.

```python
def list_orders(db, customer_id, cursor=None, limit=50):
    query = db.orders.where(customer_id=customer_id).order_by("id")
    if cursor is not None:
        query = query.where_gt("id", cursor)
    rows = query.limit(limit + 1).all()
    has_more = len(rows) > limit
    rows = rows[:limit]
    next_cursor = rows[-1].id if has_more else None
    return {"orders": rows, "next_cursor": next_cursor}
```
