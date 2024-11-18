from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Permission class that grants access only to admin (staff) users.
    """
    def has_permission(self, request, view):
        """
        Check if the user is a staff member to access a view.
        """
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a staff member for object-level access.
        """
        return request.user.is_staff

class IsCreator(permissions.BasePermission):
    """
    Permission class that allows access only to the creator of an offer object.
    """
    def has_permission(self, request, view):
        """
        Returns True for detail requests to handle them by 'has_object_permission'.
        """
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the creator of the object for access permissions.
        """
        return obj.business_profile.user == request.user
        
class PatchAsCreator(permissions.BasePermission):
    """
    Permission class that grants access only for PATCH requests from the offer object's creator.
    """
    def has_permission(self, request, view):
        """
        Returns True for detail requests to handle them by 'has_object_permission'.
        """
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the request is a PATCH method and if the user is the creator of the offer object.
        """
        if request.method == 'PATCH':
            return obj.business_profile.user == request.user
        else:
            return False
        
class IsReviewer(permissions.BasePermission):
    """
    Permission class that grants access only to the reviewer of a review object.
    """
    def has_permission(self, request, view):
        """
        Returns True for detail requests to handle them by 'has_object_permission'.
        """
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the reviewer of the review object for access permissions.
        """
        return obj.reviewer_profile.user == request.user