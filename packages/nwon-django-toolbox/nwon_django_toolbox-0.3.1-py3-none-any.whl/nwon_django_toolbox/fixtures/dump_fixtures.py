import sys
from typing import List

from django.core.management import call_command

from nwon_django_toolbox.settings import NWON_DJANGO_SETTINGS
from nwon_django_toolbox.typings.test_fixture import Fixture


def dump_fixtures(fixture_files: List[Fixture]):
    sys_out = sys.stdout

    for fixture in fixture_files:
        sys.stdout = open(
            fixture.path, "w", encoding=NWON_DJANGO_SETTINGS.file_encoding
        )
        call_command("dumpdata", fixture.model_name)

    sys.stdout = sys_out


__all__ = [
    "dump_fixtures",
]
