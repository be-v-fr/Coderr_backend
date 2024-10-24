from django.contrib import admin
from users_app.models import UserProfile, BusinessUserProfile 

admin.site.register(UserProfile)
admin.site.register(BusinessUserProfile)