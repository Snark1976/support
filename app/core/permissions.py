from rest_framework.permissions import BasePermission


class PermissionTicketView(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            if request.user.is_staff:
                return True
            return False
        else:
            if obj.author == request.user or request.user.is_staff:
                return True
            return False
