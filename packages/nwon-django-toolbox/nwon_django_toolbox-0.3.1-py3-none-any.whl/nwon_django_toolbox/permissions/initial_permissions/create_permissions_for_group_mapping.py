# pylint: disable=unused-argument

from enum import Enum
from typing import Type, TypeVar

from nwon_django_toolbox.permissions.initial_permissions.assign_permissions_to_groups import (
    assign_permissions_to_groups,
)
from nwon_django_toolbox.permissions.initial_permissions.create_groups import (
    create_groups_from_enum,
)
from nwon_django_toolbox.permissions.initial_permissions.create_permissions_for_apps import (
    create_permissions_for_apps,
)
from nwon_django_toolbox.typings import PermissionConfiguration

T = TypeVar("T", bound=Enum)


def create_permissions_for_group_mapping(
    permission_groups: Type[T],
    permission_configuration: PermissionConfiguration[T],
    apps=None,
):
    """
    Main entrypoint for assigning permission to groups based on a mapping.

    permission_groups should be an enum consisting the group names you want to map.

    permission_configuration is a dictionary mapping a group onto a list of permissions
    for different models.

    Can be hooked into a migration.
    """

    create_groups_from_enum(permission_groups)

    if apps:
        create_permissions_for_apps(apps)

    assign_permissions_to_groups(permission_groups, permission_configuration)
