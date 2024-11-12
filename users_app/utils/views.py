from rest_framework import status
from rest_framework.response import Response
from users_app.api.serializers import UserSerializer
from .profiles import get_profile_serializer

def get_profile_update_data(profile, request_data):
    """
    Prepares data for updating the user's profile by merging current username and request data.

    :param profile: The user's profile.
    :type profile: AbstractUserProfile
    :param request_data: The data received from the request for updating the profile.
    :type request_data: dict
    :return: A dictionary with the merged update data.
    :rtype: dict
    """
    data = {'username': profile.user.username}
    data.update({key: value for key, value in request_data.items()})
    return data

def update_user(user, data):
    """
    Updates user information using the provided data and returns validation errors if any.

    :param user: The user to be updated.
    :type user: User
    :param data: The data to update the user with.
    :type data: dict
    :return: None if successful, otherwise validation errors.
    :rtype: None or dict
    """
    serializer = UserSerializer(user, data=data)
    try:
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    except:
        return serializer.errors
    return None

def update_profile_w_user(profile, request):
    """
    Updates both the user and profile data based on the request, handling validation and responses.

    :param profile: The user's profile to update.
    :type profile: AbstractUserProfile
    :param request: The HTTP request containing data for updating.
    :type request: HttpRequest
    :return: A Response object indicating success or failure of the update.
    :rtype: Response
    """
    data = get_profile_update_data(profile, request_data=request.data)
    user_errors = update_user(user=profile.user, data=data)
    if user_errors:
        return Response(user_errors, status=status.HTTP_400_BAD_REQUEST)  
    profile_serializer = get_profile_serializer(request, profile, data)
    if profile_serializer.is_valid(raise_exception=True):
        profile_serializer.save()
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)