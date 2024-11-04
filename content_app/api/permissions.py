from rest_framework import permissions
        
class PatchAsCreator(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return obj.business_profile.user == request.user
        else:
            return False
        
class PatchAsReviewer(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return obj.reviewer_profile.user == request.user
        else:
            return False