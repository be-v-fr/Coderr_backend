from django.db import models
from django.contrib.auth.models import User

def get_user_field(related_name):
    return models.OneToOneField(User, on_delete=models.CASCADE, related_name=related_name, blank=True, null=True)