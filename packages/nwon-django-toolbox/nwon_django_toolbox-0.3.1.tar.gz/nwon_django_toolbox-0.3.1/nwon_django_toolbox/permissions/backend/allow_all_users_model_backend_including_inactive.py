from django.contrib.auth.backends import AllowAllUsersModelBackend
from django.contrib.auth.models import Permission


class AllowAllUsersModelBackendIncludingInactive(AllowAllUsersModelBackend):
    """
    Permission backend that grants the same permissions fo active and inactive user.

    Default behavior is that inactive user don't get any permissions at all.
    """

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = "_%s_perm_cache" % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, "_get_%s_permissions" % from_name)(user_obj)
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(
                user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms}
            )
        return getattr(user_obj, perm_cache_name)

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous or obj is not None:
            return set()

        if not hasattr(user_obj, "_perm_cache"):
            user_obj._perm_cache = {
                *self.get_user_permissions(user_obj, obj=obj),
                *self.get_group_permissions(user_obj, obj=obj),
            }

        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj=obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Return True if user_obj has any permissions in the given app_label.
        """
        return any(
            perm[: perm.index(".")] == app_label
            for perm in self.get_all_permissions(user_obj)
        )

    def with_perm(self, perm, is_active=None, include_superusers=True, obj=None):
        return super().with_perm(perm, is_active, include_superusers, obj)
