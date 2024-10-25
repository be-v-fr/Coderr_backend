from django.contrib.auth.models import User
from .models import CustomerProfile, BusinessProfile
from .api.serializers import CustomerProfileSerializer, BusinessProfileSerializer


def get_profile(user_pk):
    user = User.objects.get(pk=user_pk)
    try:
        profile = CustomerProfile.objects.get(user=user)
    except CustomerProfile.DoesNotExist:
        profile = BusinessProfile.objects.get(user=user)
    finally:
        return profile
    
    
def get_profile_serializer_plain(profile):
    if isinstance(profile, CustomerProfile):
        return CustomerProfileSerializer(profile)
    elif isinstance(profile, BusinessProfile):
        return BusinessProfileSerializer(profile)
        
        
def get_profile_serializer_with_data(profile, data):
    if isinstance(profile, CustomerProfile):
        return CustomerProfileSerializer(profile, data=data, partial=True)
    elif isinstance(profile, BusinessProfile):
        return BusinessProfileSerializer(profile, data=data, partial=True)
    

def get_profile_serializer(request, profile):
    if request.method == 'PATCH':
        return get_profile_serializer_with_data(profile, data=request.data)
    else:
        return get_profile_serializer_plain(profile)