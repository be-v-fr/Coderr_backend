from rest_framework import permissions
from users_app.models import BusinessProfile, CustomerProfile

class ReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class ProfilePermission(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'PATCH':
            return obj.user == request.user or request.user.is_staff
        else:
            return False

class PostAsBusinessUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                profile = BusinessProfile.objects.get(user=request.user.pk)
                return True
            except BusinessProfile.DoesNotExist:
                return False
        else:
            return False

class PostAsCustomerUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                profile = CustomerProfile.objects.get(user=request.user.pk)
                return True
            except BusinessProfile.DoesNotExist:
                return False
        else:
            return False