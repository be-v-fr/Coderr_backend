from django.db.models import Avg
from rest_framework import serializers
from users_app.models import BusinessProfile
from content_app.models import Offer, CustomerReview

class BaseInfoSerializer(serializers.Serializer):
    """
    A serializer for providing general application statistics, such as counts
    of reviews, average rating, business profiles, and offers.

    Attributes:
        review_count (SerializerMethodField): The total number of customer reviews.
        average_rating (SerializerMethodField): The average rating across all reviews.
        business_profile_count (SerializerMethodField): The total number of business profiles.
        offer_count (SerializerMethodField): The total number of offers available.
    """
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()
    
    def get_review_count(self, obj):
        return CustomerReview.objects.count()

    def get_average_rating(self, obj):
        average = CustomerReview.objects.aggregate(Avg('rating'))['rating__avg']
        return f"{average:.1f}" if average is not None else '-'

    def get_business_profile_count(self, obj):
        return BusinessProfile.objects.count()

    def get_offer_count(self, obj):
        return Offer.objects.count()
