from .models import CustomerProfile, BusinessProfile
from .api.serializers import CustomerProfileSerializer, BusinessProfileSerializer


def get_profile(user):
    try:
        profile = CustomerProfile.objects.get(user=user)
    except CustomerProfile.DoesNotExist:
        profile = BusinessProfile.objects.get(user=user)
    finally:
        return profile
    

def get_serializer(request, profile):
    if profile.TYPE == CustomerProfile.TYPE:
        return CustomerProfileSerializer(profile, context={'request': request})
    elif profile.TYPE == BusinessProfile.TYPE:
        return BusinessProfileSerializer(profile, context={'request': request})