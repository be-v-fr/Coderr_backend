from rest_framework import status
from rest_framework.response import Response
from .api.serializers import UserSerializer
from .utils_profiles import get_profile_serializer

def get_profile_update_data(profile, request_data):
    data = {'username': profile.user.username}
    data.update({key: value for key, value in request_data.items()})
    return data

def update_user(user, data):
    serializer = UserSerializer(user, data=data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except:
        return serializer.errors
    return None

def update_profile_w_user(profile, request):
    data = get_profile_update_data(profile, request_data=request.data)
    user_errors = update_user(user=profile.user, data=data)
    if user_errors:
        return Response(user_errors, status=status.HTTP_400_BAD_REQUEST)  
    profile_serializer = get_profile_serializer(request, profile, data)
    if profile_serializer.is_valid(raise_exception=True):
        profile_serializer.save()
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)