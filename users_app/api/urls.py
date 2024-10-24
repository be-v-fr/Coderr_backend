from django.urls import path, include
from users_app.models import UserProfile
from .views import UserProfileViewSet

urlpatterns = [
    path('profiles/business/', UserProfileViewSet.as_view(queryset=UserProfile.objects.filter(type=UserProfile.BUSINESS)), name='business-list'),
    path('profiles/customer/', UserProfileViewSet.as_view(queryset=UserProfile.objects.filter(type=UserProfile.CUSTOMER)), name='customer-list'),
]
