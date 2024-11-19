from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from coderr_backend.utils import format_number
from users_app.models import BusinessProfile, CustomerProfile
from uploads_app.models import FileUpload
from content_app.utils.general import features_list_to_str, get_features_list_from_str

class Offer(models.Model):
    """
    Model representing an offer made by a business.

    Attributes:
        offer_type (CharField): Type of offer; can be 'basic', 'standard', or 'premium'. Defaults to 'standard'.
        offer (ForeignKey): The offer to which these details belong.
        title (CharField): Title of the offer details, up to 31 characters. Optional.
        price_cents (PositiveIntegerField): Price in cents for currency accuracy. Optional.
        features (CharField): Features of the offer, stored as a comma-separated string.
        revisions (IntegerField): Number of revisions allowed, minimum -1. Optional.
        delivery_time_in_days (PositiveIntegerField): Delivery time for the offer in days. Optional.
    """
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=63, default=None, blank=True, null=True)
    description = models.CharField(max_length=1023, default=None, blank=True, null=True)
    file = models.OneToOneField(FileUpload, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['business_profile', 'title'], name='unique_profile_title')
        ]
    
class OfferDetails(models.Model):
    """
    Model for details of an offer.

    Attributes:
        offer_type (CharField): Type of offer; can be 'basic', 'standard', or 'premium'. Defaults to 'standard'.
        offer (ForeignKey): The offer to which these details belong.
        title (CharField): Title of the offer details, up to 31 characters. Optional.
        price_cents (PositiveIntegerField): Price in cents for currency accuracy. Optional.
        features (CharField): Features of the offer, stored as a comma-separated string.
        revisions (IntegerField): Number of revisions allowed, minimum -1. Optional.
        delivery_time_in_days (PositiveIntegerField): Delivery time for the offer in days. Optional.
    """
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
    price_cents = models.PositiveIntegerField(default=None, blank=True, null=True)
    features = models.CharField(max_length=255, blank=True, default='')
    revisions = models.IntegerField(validators=[MinValueValidator(-1)], default=None, blank=True, null=True)
    delivery_time_in_days = models.PositiveIntegerField(default=None, blank=True, null=True)
    
    @property
    def price(self):
        """
        Returns the price with two decimals in a dollar/euro format.
        """
        return format_number(self.price_cents / 100, 2)

    @price.setter
    def price(self, value):
        """
        Sets the price in cents from a dollar/euro format.
        """
        self.price_cents = int(float(value) * 100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['offer_type', 'offer'], name='unique_offer_offer_type')
        ]
        
    def get_features_list(self):
        """
        Converts the features string to a list format.

        Returns:
            list: List of features.
        """
        return get_features_list_from_str(self.features)

    def set_features_str(self, features_list):
        """
        Converts a list of features to a double-comma-separated string.

        Args:
            features_list (list): List of features.
        """
        self.features = features_list_to_str(features_list)
        
class Order(models.Model):
    """
    Model representing a customer order for an offer.

    Attributes:
        status (CharField): Status of the order; can be 'in_progress', 'completed', or 'cancelled'. Defaults to 'in_progress'.
        orderer_profile (ForeignKey): The customer who placed the order.
        business_profile (ForeignKey): The business providing the order.
        title (CharField): Title of the order, up to 63 characters. Optional.
        offer_details (ForeignKey): Details of the ordered offer. Can be null if deleted.
        created_at (DateTimeField): Timestamp of order creation.
        updated_at (DateTimeField): Timestamp of last order update.
        price (CharField): Price of the order in string format. Optional.
        features (CharField): Features of the order, stored as a comma-separated string.
        revisions (IntegerField): Number of allowed revisions. Minimum -1.
        delivery_time_in_days (PositiveIntegerField): Delivery time in days.
    """
    IN_PROGRESS, COMPLETED, CANCELLED = 'in_progress', 'completed', 'cancelled'
    STATUS_CHOICES = (
            (IN_PROGRESS, _(IN_PROGRESS)),
            (COMPLETED, _(COMPLETED)),
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.CharField(max_length=8, default=None, blank=True, null=True)
    features = models.CharField(max_length=255, blank=True, default='')
    revisions = models.IntegerField(validators=[MinValueValidator(-1)], default=None, blank=True, null=True)
    delivery_time_in_days = models.PositiveIntegerField(default=None, blank=True, null=True)
    
    def get_features_list(self):
        """
        Converts the features string to a list.

        Returns:
            list: List of features.
        """
        return get_features_list_from_str(self.features)
    
class CustomerReview(models.Model):
    """
    Model representing a customer review of a business.

    Attributes:
        reviewer_profile (ForeignKey): The customer leaving the review.
        business_profile (ForeignKey): The business being reviewed. Optional.
        rating (PositiveIntegerField): Rating from 0 to 5. Optional.
        description (CharField): Text description of the review, up to 1023 characters. Optional.
        created_at (DateTimeField): Timestamp of review creation.
        updated_at (DateTimeField): Timestamp of last review update.
    """
    reviewer_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='reviews')
    business_profile = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='reviews', default=None, blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=None, blank=True, null=True)
    description = models.CharField(max_length=1023, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer_profile', 'business_profile'], name='unique_reviewer_business'),
        ]
        
    def clean(self):
        """
        Validates that a review can only be created if a corresponding order exists.

        Raises:
            ValidationError: If no matching order exists.
        """
        if not Order.objects.filter(
            business_profile=self.business_profile, 
            orderer_profile=self.reviewer_profile,
        ).exists():
            raise ValidationError(
                'A review can only be created if a corresponding order exists.'
            )

    def save(self, *args, **kwargs):
        """
        Overrides save to include custom validation.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.clean()
        super().save(*args, **kwargs)