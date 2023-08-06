import json
from os import path
from typing import List

from nwon_baseline.file_helper import read_file_content


def read_fixture_file(fixture_path: str) -> List[dict]:
    if path.isfile(fixture_path):
        return []

    fixture_json = read_file_content(fixture_path)

    if fixture_json is None:
        return []
    else:
        return json.loads(fixture_json)


__all__ = [
    "read_fixture_file",
]
