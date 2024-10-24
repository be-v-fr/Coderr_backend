from django.urls import path, include
from .views import CustomerProfileViewSet, BusinessProfileViewSet

urlpatterns = [
    path('profiles/business/', BusinessProfileViewSet.as_view(), name='business-list'),
    path('profiles/customer/', CustomerProfileViewSet.as_view(), name='customer-list'),
]
