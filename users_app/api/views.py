from rest_framework import viewsets, generics, permissions, filters
from users_app.models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(generics.ListAPIView):
    serializer_class = UserProfileSerializer