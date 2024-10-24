from django.contrib import admin
from users_app.models import CustomerProfile, BusinessProfile 

admin.site.register(CustomerProfile)
admin.site.register(BusinessProfile)