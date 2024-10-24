from django.urls import path, include
from .views import ProfileView, CustomerProfileViewSet, BusinessProfileViewSet

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfileViewSet.as_view(), name='business-list'),
    path('profiles/customer/', CustomerProfileViewSet.as_view(), name='customer-list'),
]
