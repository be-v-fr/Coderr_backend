from rest_framework import viewsets, generics, permissions, filters
from users_app.models import CustomerProfile, BusinessProfile
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer

class CustomerProfileViewSet(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    
class BusinessProfileViewSet(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer