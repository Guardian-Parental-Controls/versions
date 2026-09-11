import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))

from compile_feed import compile_feed, parse_version


def test_compile_feed_is_deterministic(tmp_path):
    components = tmp_path / 'components'
    components.mkdir()
    (components / 'agent-linux.json').write_text(
        json.dumps({
            'version': '1.0.0',
            'repository': 'https://github.com/Guardian-Parental-Controls/agent-linux',
            'artifacts': [],
        }),
        encoding='utf-8',
    )

    feed = compile_feed(components, '2026-09-11T09:00:00Z')

    assert feed['schema_version'] == 1
    assert feed['generated_at'] == '2026-09-11T09:00:00Z'
    assert feed['components']['agent-linux']['version'] == '1.0.0'


@pytest.mark.parametrize('version', ['one', '1.0', 'v1.0.x'])
def test_parse_version_rejects_invalid_semver(version):
    with pytest.raises(ValueError):
        parse_version(version)
