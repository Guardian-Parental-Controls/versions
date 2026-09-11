#!/usr/bin/env python3
"""Validate and store a component payload delivered by release CI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from compile_feed import parse_version

ALLOWED_COMPONENTS = {
    'platform',
    'agent-common',
    'agent-linux',
    'agent-windows',
    'agent-android',
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--payload', type=Path, required=True)
    parser.add_argument('--components', type=Path, default=Path('components'))
    args = parser.parse_args()

    payload = json.loads(args.payload.read_text(encoding='utf-8'))
    component_id = str(payload.pop('component', ''))
    if component_id not in ALLOWED_COMPONENTS:
        raise ValueError(f'unsupported component: {component_id}')

    parse_version(str(payload.get('version', '')))
    expected_repository = (
        f'https://github.com/Guardian-Parental-Controls/{component_id}'
    )
    if payload.get('repository') != expected_repository:
        raise ValueError(f'repository must be {expected_repository}')
    if not isinstance(payload.get('artifacts'), list):
        raise ValueError('artifacts must be a list')

    args.components.mkdir(parents=True, exist_ok=True)
    output = args.components / f'{component_id}.json'

    if output.exists():
        current = json.loads(output.read_text(encoding='utf-8'))
        if parse_version(str(payload['version'])) < parse_version(str(current['version'])):
            raise ValueError('refusing to replace a component with an older version')

    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
