from django.db import models
from django.contrib.auth.models import User

def get_user_field(related_name):
    """
    Helper function to generate the user field for user profile models.
    
    :param related_name: Reference from user field to associated profile.
    :type related_name: str
    :return: User field.
    :rtype: models.OneToOneField
    """
    return models.OneToOneField(User, on_delete=models.CASCADE, related_name=related_name, blank=True, null=True)