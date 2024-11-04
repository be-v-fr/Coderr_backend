from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users_app.api.urls')),
    path('api/', include('content_app.api.urls')),
    path('api/', include('statistics_app.api.urls')),
]
