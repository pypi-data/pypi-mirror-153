from enum import Enum
from typing import List, Type

from django.contrib.auth.models import Group


def create_groups_from_enum(permission_groups: Type[Enum]) -> List[Group]:
    return [
        Group.objects.get_or_create(name=group_name.value)[0]
        for group_name in permission_groups
    ]
