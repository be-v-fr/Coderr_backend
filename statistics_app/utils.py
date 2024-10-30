from django.contrib.auth.models import User
from users_app.models import BusinessProfile
from content_app.models import Order

def get_business_user_orders(user_id):
    try:
        user = User.objects.get(pk=user_id)
        business_profile = BusinessProfile.objects.get(user=user)
        return Order.objects.filter(business_profile=business_profile)
    except:
        return None