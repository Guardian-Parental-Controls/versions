# Guardian versions

This repository compiles the public Guardian release catalog. `feed.json` is
the sole source of truth for current component versions, repositories, and
release artifacts.

Routine component records are written by release pipelines through
`repository_dispatch`; do not edit `components/*.json` or `feed.json` by hand.

## Local validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/compile_feed.py
python -m jsonschema --instance feed.json schema/feed.schema.json
python -m pytest -q
```

The production feed is published at:

<https://guardian-parental-controls.github.io/versions/feed.json>
