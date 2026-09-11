#!/usr/bin/env python3
"""Compile the auditable Guardian release feed from CI-managed components."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_version(value: str) -> tuple[int, int, int]:
    core = value.strip().lstrip('v').split('-', 1)[0].split('+', 1)[0]
    parts = core.split('.')
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError(f'invalid semantic version: {value}')
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def compile_feed(components_dir: Path, generated_at: str | None = None) -> dict[str, Any]:
    components: dict[str, dict[str, Any]] = {}
    for component_path in sorted(components_dir.glob('*.json')):
        component = json.loads(component_path.read_text(encoding='utf-8'))
        component_id = component_path.stem
        if component_id in components:
            raise ValueError(f'duplicate component: {component_id}')
        parse_version(str(component.get('version', '')))
        components[component_id] = component

    if not components:
        raise ValueError('at least one component record is required')

    timestamp = generated_at or datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    return {
        'schema_version': 1,
        'generated_at': timestamp,
        'components': components,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--components', type=Path, default=Path('components'))
    parser.add_argument('--output', type=Path, default=Path('feed.json'))
    parser.add_argument('--generated-at')
    args = parser.parse_args()

    feed = compile_feed(args.components, args.generated_at)
    args.output.write_text(
        json.dumps(feed, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
