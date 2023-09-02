from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """ Permissions that allow modifying data only to the owner. """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
