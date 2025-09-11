"""A module that implements custom made permissions."""
from rest_framework.permissions import BasePermission

class AdminUser(BasePermission):
    """Checks if a user has the role of an Admin."""
    def has_permission(self, request, view):
        user = request.user
        print(user)
        return user.role == 'admin'