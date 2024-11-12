from django.urls import path
from .views import LoginView, RegistrationView, ProfileView, CustomerProfileViewSet, BusinessProfileViewSet

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessProfileViewSet.as_view(), name='business-list'),
    path('profiles/customer/', CustomerProfileViewSet.as_view(), name='customer-list'),
]
