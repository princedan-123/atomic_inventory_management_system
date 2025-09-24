"""A module that implements custom made permissions."""
from rest_framework.permissions import BasePermission

class AdminUser(BasePermission):
    """Checks if a user has the role of an Admin."""
    def has_permission(self, request, view):
        user = request.user
        return user.role == 'admin'

class IsStockManager(BasePermission):
    """Checks if a user is a stock manager."""
    def has_permission(self, request, view):
        user = request.user
        return user.role == 'stock manager'

class IsAgent(BasePermission):
    """Checks if user is an agent."""
    def has_permission(self, request, view):
        user = request.user
        return user.role == 'agent'