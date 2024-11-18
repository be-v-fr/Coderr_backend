from rest_framework import permissions
from users_app.models import BusinessProfile, CustomerProfile

class ReadOnly(permissions.BasePermission):
    """
    Allows read-only access for any request method classified as safe (e.g., GET, HEAD, OPTIONS).

    Methods:
        has_permission(request, view): Checks if the request method is read-only.
        has_object_permission(request, view, obj): Checks if the object-specific request is read-only.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class ProfilePermission(permissions.BasePermission):
    """
    Allows safe method access, and permits PATCH if the user is the owner or has staff status.

    Methods:
        has_object_permission(request, view, obj): Checks object-level permissions based on the request method.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'PATCH':
            return obj.user == request.user or request.user.is_staff
        else:
            return False

class PostAsBusinessUser(permissions.BasePermission):
    """
    Allows POST requests only for users with a BusinessProfile.

    Methods:
        has_permission(request, view): Checks if the request user has a BusinessProfile and is making a POST request.
    """
    def has_permission(self, request, view):
        if (
            request.method == 'POST'
            and request.user.is_authenticated
            and BusinessProfile.objects.filter(user=request.user.pk).exists()
        ):
            return True
        return False

class PostAsCustomerUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if (
            request.method == 'POST'
            and request.user.is_authenticated
            and CustomerProfile.objects.filter(user=request.user.pk).exists()
        ):
            return True
        return False