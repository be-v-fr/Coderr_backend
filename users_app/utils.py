from .models import CustomerProfile, BusinessProfile
from .api.serializers import CustomerProfileSerializer, BusinessProfileSerializer


def get_profile_or_none(user):
    try:
        profile = CustomerProfile.objects.get(user=user)
    except CustomerProfile.DoesNotExist:
        try:
            profile = BusinessProfile.objects.get(user=user)
        except BusinessProfile.DoesNotExist:
            profile = None
    finally:
        return profile
    

def get_serializer(request, profile):
    if profile.TYPE == CustomerProfile.TYPE:
        return CustomerProfileSerializer(profile, context={'request': request})
    elif profile.TYPE == BusinessProfile.TYPE:
        return BusinessProfileSerializer(profile, context={'request': request})