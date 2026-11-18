---
tags: [surgical-edits]
runs: 3
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

We changed the default port from 8080 to 9090 in the last release. Update the
README below and give me the full updated file.

````markdown
# pantry

pantry is a tiny inventory server. you point it at a folder of YAML and it
serves that folder as an API. that's the whole trick.

## requirements

Node 16 or newer.

## getting going

```bash
npm install -g pantry
pantry serve ./stock
```

then poke it:

```bash
curl http://localhost:8080/items
```

## knobs

| flag | default | what it does |
| --- | --- | --- |
| `--port` | `8080` | port to listen on |
| `--watch` | off | reload when the YAML changes |
| `--cors` | off | send permissive CORS headers |

## notes

we only test on Node 18 and 20, so anything older is on you.
````
