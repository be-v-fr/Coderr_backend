from django.db import models
from django.contrib.auth.models import User
from uploads_app.models import FileUpload

def get_user_field(related_name):
    return models.OneToOneField(User, on_delete=models.CASCADE, related_name=related_name, blank=True, null=True)
    
class AbstractUserProfile(models.Model):
    TYPE = None
    
    user = get_user_field(related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.OneToOneField(FileUpload, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        """
        Returns the string representation of the UserProfile, showing the ID and username.
        """
        return f"({self.id}) {self.user.username}"
    
class CustomerProfile(AbstractUserProfile):
    TYPE = 'customer'
    user = get_user_field(related_name='customer_profile')
    
class BusinessProfile(AbstractUserProfile):
    TYPE = 'business'
    user = get_user_field(related_name='business_profile')
    location = models.CharField(max_length=32, default=None, blank=True, null=True)
    description = models.CharField(max_length=1024, default=None, blank=True, null=True)
    working_hours = models.CharField(max_length=32, default=None, blank=True, null=True)
    tel = models.CharField(max_length=32, default=None, blank=True, null=True)