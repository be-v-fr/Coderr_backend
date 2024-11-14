from django.contrib.auth.models import User
from users_app.models import BusinessProfile
from content_app.models import Order

def get_business_user_orders(user_id):
    """
    Retrieves all orders associated with a business profile for a given user.

    Args:
        user_id (int): The ID of the user whose business orders are being retrieved.
    """
    business_profile = User.objects.get(pk=user_id).business_profile
    return Order.objects.filter(business_profile=business_profile)
