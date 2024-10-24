from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import datetime
    
class UserProfile(models.Model):
    CUSTOMER, BUSINESS = ('customer', 'business')
    TYPES = (
            (CUSTOMER, _('Customer')),
            (BUSINESS, _('Business')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=16,
        choices=TYPES,
        default=CUSTOMER,
    )
    created_at = models.DateField(default=datetime.date.today)
    file = models.CharField(max_length=64, default=None, blank=True, null=True)
    uploaded_at = models.DateField(default=None, blank=True, null=True)

    
    def __str__(self):
        """
        Returns the string representation of the UserProfile, showing the ID and username.
        """
        return f"({self.id}) {self.user.username}"
    
class BusinessUserProfile(UserProfile):
    location = models.CharField(max_length=32, default=None, blank=True, null=True)
    description = models.CharField(max_length=1024, default=None, blank=True, null=True)
    working_hours = models.CharField(max_length=32, default=None, blank=True, null=True)
    tel = models.CharField(max_length=32, default=None, blank=True, null=True)