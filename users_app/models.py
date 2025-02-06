from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os
import six
from uploads_app.models import FileUpload
from .utils.models import get_user_field, send_account_activation_email
    
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
    location = models.CharField(max_length=32, default='', blank=True, null=True)
    description = models.CharField(max_length=1024, default='', blank=True, null=True)
    working_hours = models.CharField(max_length=32, default='', blank=True, null=True)
    tel = models.CharField(max_length=32, default='', blank=True, null=True)

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation for better stability and code readability.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

class UserAction(models.Model):
    """
    Abstract model connecting a user to a token.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        unique_together = ('token', 'user')
        
    def __str__(self):
        return f"{self.user.email} ({self.created_at})"

    def is_token_expired(self):
        """
        Checks token expiration date.
        """
        expiration_time = self.created_at + timedelta(hours=24)
        return now() > expiration_time

    @classmethod
    def create_with_token(cls, user, token_generator_class):
        """
        Creates class instance from respective user by using a token generator.
        """
        token = token_generator_class().make_token(user)
        instance = cls(user=user, token=token)
        instance.save()
        return instance        

    @classmethod
    def delete_all_for_user(cls, user):
        """
        Deletes all class instances for the respective user.
        """
        instances = cls.objects.filter(user=user)
        instances.delete()

class AccountActivation(UserAction):
    """
    Account activation model including user email and token.
    """
    @classmethod
    def create_with_email(cls, user):
        """
        Creates class instance and sends corresponding email to the respective user.
        """
        instance = cls.create_with_token(user, AccountActivationTokenGenerator)
        activation_url = os.environ['FRONTEND_BASE_URL'] + '?activate=' + instance.token
        send_account_activation_email(recipient=instance.user.email, activation_url=activation_url)
        return instance