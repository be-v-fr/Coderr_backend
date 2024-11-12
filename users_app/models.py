from django.db import models
from uploads_app.models import FileUpload
from .utils.models import get_user_field
    
class AbstractUserProfile(models.Model):
    """
    An abstract base model for user profiles with common attributes.

    Attributes:
        TYPE: Defines the profile type, should be specified in subclasses.
        user: The user associated with the profile.
        created_at: The timestamp when the profile was created.
        file: A file associated with the profile, stored in FileUpload.
    """
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
    """
    A profile model for customers, extending AbstractUserProfile.

    Attributes:
        TYPE: The type of profile, set to 'customer'.
        user: The user associated with this customer profile.
    """
    TYPE = 'customer'
    user = get_user_field(related_name='customer_profile')
    
class BusinessProfile(AbstractUserProfile):
    """
    A profile model for businesses, extending AbstractUserProfile, with additional business-specific fields.

    Attributes:
        TYPE: The type of profile, set to 'business'.
        user: The user associated with this business profile.
        location: The location of the business.
        description: A description of the business.
        working_hours: The business's working hours.
        tel: The business's contact phone number.
    """
    TYPE = 'business'
    user = get_user_field(related_name='business_profile')
    location = models.CharField(max_length=32, default=None, blank=True, null=True)
    description = models.CharField(max_length=1024, default=None, blank=True, null=True)
    working_hours = models.CharField(max_length=32, default=None, blank=True, null=True)
    tel = models.CharField(max_length=32, default=None, blank=True, null=True)