from django.contrib.auth.models import User
from users_app.models import CustomerProfile, BusinessProfile
from users_app.api.serializers import CustomerProfileDetailSerializer, BusinessProfileDetailSerializer

def get_profile(user_pk):
    """
    Retrieves the user profile (CustomerProfile or BusinessProfile) associated with the given user primary key.

    :param user_pk: The primary key of the user.
    :type user_pk: int
    :return: The associated profile (CustomerProfile or BusinessProfile).
    :rtype: CustomerProfile or BusinessProfile
    """
    user = User.objects.get(pk=user_pk)
    try:
        profile = CustomerProfile.objects.get(user=user)
    except CustomerProfile.DoesNotExist:
        profile = BusinessProfile.objects.get(user=user)
    finally:
        return profile
    
    
def get_profile_serializer_plain(profile):
    """
    Returns the appropriate serializer for a given profile without additional data.

    :param profile: The profile to serialize.
    :type profile: CustomerProfile or BusinessProfile
    :return: The serializer for the given profile.
    :rtype: CustomerProfileDetailSerializer or BusinessProfileDetailSerializer
    """
    if isinstance(profile, CustomerProfile):
        return CustomerProfileDetailSerializer(profile)
    elif isinstance(profile, BusinessProfile):
        return BusinessProfileDetailSerializer(profile)
        
        
def get_profile_serializer_with_data(profile, data):
    """
    Returns the appropriate serializer for a given profile with additional data for partial updates.

    :param profile: The profile to serialize.
    :type profile: CustomerProfile or BusinessProfile
    :param data: The data to partially update the profile.
    :type data: dict
    :return: The serializer with the given profile and data.
    :rtype: CustomerProfileDetailSerializer or BusinessProfileDetailSerializer
    """
    if isinstance(profile, CustomerProfile):
        return CustomerProfileDetailSerializer(profile, data=data, partial=True)
    elif isinstance(profile, BusinessProfile):
        return BusinessProfileDetailSerializer(profile, data=data, partial=True)
    

def get_profile_serializer(request, profile, data):
    """
    Returns the appropriate serializer for a profile based on the HTTP method in the request.

    :param request: The HTTP request object containing the method.
    :type request: HttpRequest
    :param profile: The profile to serialize.
    :type profile: CustomerProfile or BusinessProfile
    :param data: The data to potentially update the profile (for PATCH requests).
    :type data: dict
    :return: The serializer for the given profile, with or without data.
    :rtype: CustomerProfileDetailSerializer or BusinessProfileDetailSerializer
    """
    if request.method == 'PATCH':
        return get_profile_serializer_with_data(profile, data=data)
    else:
        return get_profile_serializer_plain(profile)