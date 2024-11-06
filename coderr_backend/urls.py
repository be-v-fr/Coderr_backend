from django.contrib import admin
from django.urls import path, include

API_BASE_URL = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE_URL, include('users_app.api.urls')),
    path(API_BASE_URL, include('content_app.api.urls')),
    path(API_BASE_URL, include('statistics_app.api.urls')),
]
