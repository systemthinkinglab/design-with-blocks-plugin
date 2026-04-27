# render/

PNG renderer for system design diagrams produced by `/design-with-blocks`.

## Files

- `render.py` — main renderer (single self-contained Python script)
- `icons/` — the 10 canonical building-block + entity icons used in the videos
- `requirements.txt` — Python dependencies

## Install (one-time)

```bash
pip install -r requirements.txt
```

Both Claude Code and claude.ai code-interpreter sandboxes already have these installed in most cases (Pillow, networkx, numpy, scipy).

## Usage

### From Python

```python
from render import render

design = {
    "title": "My Recipe App",
    "nodes": [
        {"id": "user", "type": "user", "label": "User"},
        {"id": "svc",  "type": "service", "label": "Recipe Service",
         "tech": "Render Web Service"},
        {"id": "db",   "type": "relational_database", "label": "Recipe DB",
         "tech": "Postgres"},
    ],
    "edges": [
        {"from": "user", "to": "svc"},
        {"from": "svc",  "to": "db"},
    ],
}

render(design, "architecture.png")
```

### From the command line

```bash
# Read from a file
python render.py design.json -o architecture.png

# Read from stdin
cat design.json | python render.py - -o architecture.png

# Render the bundled sample
python render.py --sample -o architecture.png
```

## Design JSON schema

```jsonc
{
  "title": "App Architecture",        // optional, shown at top of PNG

  "nodes": [
    {
      "id": "unique_id",              // referenced by edges
      "type": "service",              // one of the 10 known types (see below)
      "label": "Recipe Service",      // pattern + functionality, NO technology
      "tech": "Render Web Service"    // optional; appears in tech-choices table
    }
  ],

  "edges": [
    { "from": "id_a", "to": "id_b" }  // arrow direction matters
  ]
}
```

### Valid `type` values

| Category | Type values |
|----------|-------------|
| Task primitives | `service`, `worker` |
| Storage primitives | `queue`, `key_value_store`, `file_store`, `relational_database`, `vector_database` |
| External entities | `user`, `external_service`, `time` |

These are the only 10 valid types — the framework's invariant. Inventing new types is intentionally not supported.

## Label conventions

The diagram labels should describe the **pattern and functionality**, not the technology. The technology lives in the `tech` field and renders in a separate "Technology choices" table beneath the legend. Examples:

| Good label | Tech field |
|------------|-----------|
| `Recipe Service` | `Render Web Service` |
| `Cache` | `Redis` |
| `Recipe DB` | `Postgres` |
| `User Photos` | `S3` |
| `Photo Jobs` | `BullMQ` |
| `Time` | `Cron` |
| `Payments` | `Stripe` |

This separation reinforces the framework's "patterns first, technology second" stance.
