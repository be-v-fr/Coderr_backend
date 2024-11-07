from django_filters import rest_framework as filters
from content_app.models import Offer, CustomerReview

class OfferFilter(filters.FilterSet):
    creator_id = filters.NumberFilter(method='filter_by_creator_id')
    min_price = filters.NumberFilter(method='filter_by_min_price')
    min_delivery_time = filters.NumberFilter(method='filter_by_min_delivery_time')
    
    class Meta:
        model = Offer
        fields = ['min_price', 'min_delivery_time', 'creator_id']

    def filter_by_creator_id(self, queryset, name, value):
        return queryset.filter(business_profile__user__pk=value)
    
    def filter_by_min_price(self, queryset, name, value):
        cents = value * 100
        return queryset.filter(details__price_cents__lte=cents)

    def filter_by_min_delivery_time(self, queryset, name, value):
        return queryset.filter(details__delivery_time_in_days__lte=value)
    

class CustomerReviewFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(field_name='business_profile__user__id')
    reviewer_id = filters.NumberFilter(field_name='reviewer_profile__user__id')

    class Meta:
        model = CustomerReview
        fields = ['business_user_id', 'reviewer_id']