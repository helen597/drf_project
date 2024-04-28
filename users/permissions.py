from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="managers").exists()


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if object.owner == request.user:
            return True
        return False
