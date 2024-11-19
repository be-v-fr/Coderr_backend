from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from uploads_app.utils import handle_file_update
from users_app.utils.views import update_profile_w_user
from users_app.utils.profiles import get_profile, get_profile_serializer
from users_app.models import CustomerProfile, BusinessProfile
from .serializers import LoginSerializer, RegistrationSerializer, CustomerProfileListSerializer, BusinessProfileListSerializer
from .permissions import ProfilePermission, ReadOnly

class LoginView(APIView):
    """
    API endpoint for user login.

    Permission:
        AllowAny: Accessible to all users.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Authenticates the user and returns a response with authentication data.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    """
    API endpoint for user registration.

    Permission:
        AllowAny: Accessible to all users.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Registers a new user, creating a profile and returning response data.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class ProfileView(APIView):
    """
    API endpoint for retrieving or updating a user profile.

    Permission:
        ProfilePermission: Ensures permissions based on request method.
    """
    permission_classes = [ProfilePermission]
             
    def get(self, request, pk, format=None):
        """
        Retrieves profile data for the specified user.
        """
        try:
            profile = get_profile(user_pk=pk)
        except:
            return Response({'user': 'Benutzer oder Profil wurde nicht gefunden.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = get_profile_serializer(request, profile, data=request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)       

    def patch(self, request, pk, format=None):
        """
        Updates the user's profile and handles file uploads.
        """
        profile = get_profile(user_pk=pk)
        self.check_object_permissions(request, profile)
        upload_error = handle_file_update(obj=profile, data_dict=request.data, file_key='file')
        if upload_error:
            return Response(upload_error, status=status.HTTP_400_BAD_REQUEST)
        return update_profile_w_user(profile, request)
    
class CustomerProfileViewSet(generics.ListAPIView):
    """
    ViewSet for listing CustomerProfile instances.

    Permission:
        ReadOnly: Allows read-only access to customer profiles.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileListSerializer
    permission_classes = [ReadOnly]
    
class BusinessProfileViewSet(generics.ListAPIView):
    """
    ViewSet for listing BusinessProfile instances.

    Permission:
        ReadOnly: Allows read-only access to business profiles.
    """
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileListSerializer
    permission_classes = [ReadOnly]