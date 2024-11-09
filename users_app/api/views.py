from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from users_app.utils_profiles import get_profile, get_profile_serializer
from users_app.models import CustomerProfile, BusinessProfile
from .serializers import USER_FIELDS
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, CustomerProfileListSerializer, BusinessProfileListSerializer
from .permissions import ProfilePermission, ReadOnly

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ProfileView(APIView):
    permission_classes = [ProfilePermission]
             
    def get(self, request, pk, format=None):
        try:
            profile = get_profile(user_pk=pk)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = get_profile_serializer(request, profile, data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)       

    def patch(self, request, pk, format=None):
        try:
            profile = get_profile(user_pk=pk)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        data = {'username': profile.user.username}
        data.update({key: value for key, value in request.data.items()})
        user_serializer = UserSerializer(profile.user, data=data)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        profile_serializer = get_profile_serializer(request, profile, data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class CustomerProfileViewSet(generics.ListAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileListSerializer
    permission_classes = [ReadOnly]
    
class BusinessProfileViewSet(generics.ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileListSerializer
    permission_classes = [ReadOnly]