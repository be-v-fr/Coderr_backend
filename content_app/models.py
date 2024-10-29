from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from users_app.models import BusinessProfile, CustomerProfile
from content_app.utils import features_list_to_str
from datetime import date

class Offer(models.Model):
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business_profile_set')
    title = models.CharField(max_length=63, default=None, blank=True, null=True)
    description = models.CharField(max_length=1023, default=None, blank=True, null=True)
    image = models.CharField(max_length=63, default=None, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    updated_at = models.DateField(default=date.today)
    min_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_delivery_time = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business_profile', 'title'], name='unique_profile_title')
        ]
    
class OfferDetails(models.Model):
    BASIC, STANDARD, PREMIUM = 'basic', 'standard', 'premium'
    OFFER_TYPES = (
            (BASIC, _(BASIC)),
            (STANDARD, _(STANDARD)),
            (PREMIUM, _(PREMIUM)),
    )
    offer_type = models.CharField(
        max_length=16,
        choices=OFFER_TYPES,
        default=STANDARD,
    )
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=31, default=None, blank=True, null=True)
    price = models.PositiveIntegerField(default=None, blank=True, null=True)
    features = models.CharField(max_length=255, blank=True, default='')
    revisions = models.PositiveIntegerField(validators=[MinValueValidator(-1)], default=None, blank=True, null=True)
    delivery_time_in_days = models.PositiveIntegerField(default=None, blank=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['offer_type', 'offer'], name='unique_offer_offer_type')
        ]
        
    def get_features_list(self):
        return self.features.split(',,') if self.features else []

    def set_features_str(self, features_list):
        self.features = features_list_to_str(features_list)
        
class Order(models.Model):
    IN_PROGRESS, COMPLETE, CANCELLED = 'in_progress', 'complete', 'cancelled'
    STATUS_CHOICES = (
            (IN_PROGRESS, _(IN_PROGRESS)),
            (COMPLETE, _(COMPLETE)),
            (CANCELLED, _(CANCELLED)),
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=IN_PROGRESS,
    )
    orderer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='orders')
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=63, default=None, blank=True, null=True)
    offer_details = models.ForeignKey(OfferDetails, on_delete=models.SET_NULL, related_name='orders', default=None, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    updated_at = models.DateField(default=date.today)
    price = models.PositiveIntegerField(default=None, blank=True, null=True)
    features = models.CharField(max_length=255, blank=True, default='')
    revisions = models.PositiveIntegerField(validators=[MinValueValidator(-1)], default=None, blank=True, null=True)
    delivery_time_in_days = models.PositiveIntegerField(default=None, blank=True, null=True)
    
class CustomerReview(models.Model):
    reviewer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='reviews')
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='reviews', default=None, blank=True, null=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews', default=None, blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=None, blank=True, null=True)
    description = models.CharField(max_length=1023, default=None, blank=True, null=True)
    created_at = models.DateField(default=date.today)
    updated_at = models.DateField(default=date.today)