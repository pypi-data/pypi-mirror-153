from django.contrib.auth.management import (
    create_permissions as create_django_permissions,
)


def create_permissions_for_apps(apps):
    """
    Create permissions before applying them
    """

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_django_permissions(app_config, verbosity=0)
        app_config.models_module = None
