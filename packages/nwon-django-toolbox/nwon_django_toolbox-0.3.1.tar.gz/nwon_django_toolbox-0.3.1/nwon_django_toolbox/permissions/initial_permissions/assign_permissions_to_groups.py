from enum import Enum
from typing import List, Type, TypeVar

from django.contrib.auth.models import Group, Permission

from nwon_django_toolbox.typings import (
    GroupPermissionMapping,
    PermissionConfiguration,
    PermissionConfigurationForGroup,
    PermissionPrefix,
)

T = TypeVar("T", bound=Enum)


def assign_permissions_to_groups(
    permission_groups: Type[T], permission_configuration: PermissionConfiguration[T]
):
    """
    Assign model-level permissions to maintainers
    """

    permissions_for_group = __group_permissions_mapping(
        permission_groups, permission_configuration
    )
    for group_name in permission_groups:
        Group.objects.get(name=group_name.value).permissions.add(
            *permissions_for_group[group_name]
        )


def __group_permissions_mapping(
    permission_groups: Type[T],
    permission_configuration: PermissionConfiguration[T],
) -> GroupPermissionMapping[T]:
    permissions_per_group: GroupPermissionMapping[T] = {}

    for group in permission_groups:
        permissions_per_group[group] = __permissions_for_group(
            permission_configuration[group]
        )

    return permissions_per_group


def __permissions_for_group(
    permission_configuration: PermissionConfigurationForGroup,
) -> List[Permission]:
    permission_list: List[Permission] = []

    for permission_prefix in PermissionPrefix:
        permission_list = permission_list + __permissions_for_group_and_prefix(
            permission_configuration, permission_prefix
        )

    return permission_list


def __permissions_for_group_and_prefix(
    permission_configuration: PermissionConfigurationForGroup,
    permission_prefix: PermissionPrefix,
) -> List[Permission]:
    relevant_permissions = Permission.objects.filter(
        content_type__app_label="tamoc",
        codename__startswith=f"{permission_prefix.value}_",
    )

    codenames = [
        f"{permission_prefix.value}_{model.__name__.lower()}"
        for model in permission_configuration[permission_prefix]
    ]

    return [
        permission
        for permission in relevant_permissions.all()
        if permission.codename in codenames
    ]
