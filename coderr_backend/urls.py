from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

API_BASE_URL = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_BASE_URL + 'auth/', include('users_app.api.urls')),
    path(API_BASE_URL + 'content/', include('content_app.api.urls')),
    path(API_BASE_URL + 'stats/', include('statistics_app.api.urls')),
    path('docs/', include('docs_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)