from django.contrib.auth.models import User
from users_app.models import BusinessProfile
from content_app.models import Order

def get_business_user_orders(user_id):
    try:
        business_profile = User.objects.get(pk=user_id).business_profile
    except:
        return None
    return Order.objects.filter(business_profile=business_profile)
