from rest_framework.permissions import BasePermission, SAFE_METHODS

def user_is_admin(user):
    return user and user.is_authenticated and (user.is_superuser or user.groups.filter(name='admin').exists())

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # read allowed to authenticated users by default permissions
        return user_is_admin(request.user)
