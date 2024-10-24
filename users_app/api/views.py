from django.contrib.auth.models import User
from rest_framework import status, viewsets, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from users_app.models import CustomerProfile, BusinessProfile
from users_app.utils import get_profile, get_serializer
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer

class ProfileView(APIView):
             
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
            profile = get_profile(user)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = get_serializer(request, profile)
        return Response(serializer.data, status=status.HTTP_200_OK)       
        
class CustomerProfileViewSet(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    
class BusinessProfileViewSet(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer