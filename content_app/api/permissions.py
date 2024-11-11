from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff

class IsCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.business_profile.user == request.user
        
class PatchAsCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return obj.business_profile.user == request.user
        else:
            return False
        
class IsReviewer(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.reviewer_profile.user == request.user