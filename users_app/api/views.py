from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from users_app.utils import get_profile, get_profile_serializer
from users_app.models import CustomerProfile, BusinessProfile
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer
from .permissions import ProfilePermission, ReadOnly

class ProfileView(APIView):
    permission_classes = [ProfilePermission]
             
    def get(self, request, pk, format=None):
        try:
            profile = get_profile(user_pk=pk)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = get_profile_serializer(request, profile)
        return Response(serializer.data, status=status.HTTP_200_OK)       

    def patch(self, request, pk, format=None):
        try:
            profile = get_profile(user_pk=pk)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = get_profile_serializer(request, profile)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class CustomerProfileViewSet(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [ReadOnly]
    
class BusinessProfileViewSet(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [ReadOnly]