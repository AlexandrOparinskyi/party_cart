from rest_framework.permissions import BasePermission


class IsOwnerOrAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin or request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_admin:
            return True
        return False
