from os import path
from typing import List

from django.core.management import call_command

from nwon_django_toolbox.typings.test_fixture import Fixture


def load_fixtures(fixture_files: List[Fixture], app_label: str):
    for fixture in fixture_files:
        if path.isfile(fixture.path):
            call_command(
                "loaddata",
                fixture.path,
                app_label=app_label,
            )


__all__ = [
    "load_fixtures",
]
