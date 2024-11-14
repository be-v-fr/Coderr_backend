from django_filters import rest_framework as filters
from content_app.models import Offer, CustomerReview

class OfferFilter(filters.FilterSet):
    """
    Filter set for the `Offer` model, allowing filtering by creator ID, minimum price, 
    and maximum delivery time.

    Attributes:
        creator_id (NumberFilter): Filters offers by the ID of the user who created the offer.
        min_price (NumberFilter): Filters offers with prices less than or equal to the specified minimum price.
        max_delivery_time (NumberFilter): Filters offers with delivery times less than or equal to the specified max delivery time.
    """
    creator_id = filters.NumberFilter(method='filter_by_creator_id')
    min_price = filters.NumberFilter(method='filter_by_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_by_max_delivery_time')
    
    class Meta:
        model = Offer
        fields = ['min_price', 'max_delivery_time', 'creator_id']

    def filter_by_creator_id(self, queryset, name, value):
        """
        Filters the offer queryset by the user ID of the creator (business profile user).

        Returns:
            QuerySet: Offer queryset filtered by the specified creator ID.
        """
        return queryset.filter(business_profile__user__pk=value)
    
    def filter_by_min_price(self, queryset, name, value):
        """
        Filters the offer queryset by a minimum price in cents, where offers have prices 
        less than or equal to the specified minimum.

        Returns:
            QuerySet: Offer queryset filtered by the specified minimum price.
        """
        cents = value * 100
        return queryset.filter(details__price_cents__lte=cents)

    def filter_by_max_delivery_time(self, queryset, name, value):
        """
        Filters the offer queryset by a maximum delivery time, where offers have delivery 
        times less than or equal to the specified maximum.

        Returns:
            QuerySet: Offer queryset filtered by the specified maximum delivery time.
        """
        return queryset.filter(details__delivery_time_in_days__lte=value)
    

class CustomerReviewFilter(filters.FilterSet):
    """
    Filter set for the `CustomerReview` model, allowing filtering by the business user 
    ID and reviewer user ID.

    Attributes:
        business_user_id (NumberFilter): Filters reviews based on the business user's ID.
        reviewer_id (NumberFilter): Filters reviews based on the reviewer user's ID.
    """
    business_user_id = filters.NumberFilter(field_name='business_profile__user__id')
    reviewer_id = filters.NumberFilter(field_name='reviewer_profile__user__id')

    class Meta:
        model = CustomerReview
        fields = ['business_user_id', 'reviewer_id']