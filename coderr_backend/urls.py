from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users_app.api.urls')),
    path('api/content/', include('content_app.api.urls')),
    path('api/stats/', include('statistics_app.api.urls')),
]
