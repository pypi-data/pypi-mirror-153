from rest_framework.permissions import BasePermission


class IsActive(BasePermission):
    """
    Allows access only to active users.
    """

    def has_permission(self, request, view):
        return request.user.is_active

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
