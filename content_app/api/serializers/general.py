from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import BusinessProfile, CustomerProfile
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from content_app.api.serializers.offer_details import OfferDetailsSerializer
from content_app.utils.general import get_order_create_dict
from content_app.utils.general import validate_attrs_has_only_selected_fields, validate_attrs_has_and_has_only_selected_fields
from content_app.utils.serializers import create_offer_details, update_offer_details

class OfferSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Offer model with custom fields and methods for related OfferDetails.

    Attributes:
        user (SerializerMethodField): Returns the Offer creator's user ID.
        details (OfferDetailsSerializer): Serializes nested OfferDetails objects.
        min_price (SerializerMethodField): Gets the minimum price from related OfferDetails.
        min_delivery_time (SerializerMethodField): Gets the minimum delivery time from related OfferDetails.
        image (FileField): The offer image file, read-only.
    """
    user = serializers.SerializerMethodField()
    details = OfferDetailsSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    image = serializers.FileField(source='file.file', read_only=True)
        
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        
    def to_representation(self, instance):
        """
        Updates context for details serializer with the current context.
        """
        self.fields['details'].context.update(self.context)
        return super().to_representation(instance)
        
    def get_user(self, obj):
        return obj.business_profile.user.pk
    
    def get_min_price(self, obj):
        return obj.details.order_by('price_cents').first().price if obj.details.exists() else None
    
    def get_min_delivery_time(self, obj):
        return obj.details.order_by('delivery_time_in_days').first().delivery_time_in_days if obj.details.exists() else None
    
    def validate_details(self, value):
        """
        Ensures each offer type is unique within the details.
        """
        offer_types = set()
        for detail in value:
            offer_type = detail.get('offer_type')
            if offer_type in offer_types:
                raise serializers.ValidationError('Every offer type is allowed only once.')
            offer_types.add(offer_type)  
        return value
    
    def create(self, validated_data):
        """
        Creates a new Offer as well as its associated OfferDetails.
        """
        many_details_data = validated_data.pop('details', {})
        user = User.objects.get(pk=self.context['request'].user.pk)
        profile = BusinessProfile.objects.get(user=user)
        new_offer = Offer.objects.create(business_profile=profile, **validated_data)
        for single_details_data in many_details_data:
            create_offer_details(offer_id=new_offer.pk, data=single_details_data, context=self.context)
        return new_offer
    
    def update(self, instance, validated_data):
        """
        Updates an existing Offer as well as its associated OfferDetails.
        """
        details_data = validated_data.pop('details', [])
        updated_offer = super().update(instance, validated_data)
        for single_details_data in details_data:
            update_offer_details(offer=updated_offer, data=single_details_data)
        return updated_offer
    
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Order model with custom methods to retrieve user and offer detail information.

    Attributes:
        customer_user (SerializerMethodField): ID of the customer user associated with the order.
        business_user (SerializerMethodField): ID of the business user associated with the order.
        offer_detail_id (IntegerField): Write-only field for linking to OfferDetails on creation.
        offer_type (SerializerMethodField): Type of the offer.
        features (SerializerMethodField): Features of the offer in the order.
    """
    customer_user = serializers.SerializerMethodField()
    business_user = serializers.SerializerMethodField()
    offer_detail_id = serializers.IntegerField(write_only=True)
    offer_type = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'status', 'offer_detail_id', 'offer_type', 'created_at', 'updated_at', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def get_customer_user(self, obj):
        return obj.orderer_profile.user.pk
    
    def get_business_user(self, obj):
        return obj.business_profile.user.pk
    
    def get_offer_type(self, obj):
        return obj.offer_details.offer_type
    
    def get_features(self, obj):
        return obj.get_features_list()
    
    def validate(self, attrs):
        """
        Validates required fields based on request method (POST or PATCH).
        """
        request = self.context.get('request')     
        if request and request.method == 'POST':
            validate_attrs_has_and_has_only_selected_fields(['offer_detail_id'], attrs)
        elif request and request.method == 'PATCH':
            validate_attrs_has_and_has_only_selected_fields(['status'], attrs)
        return attrs

    def create(self, validated_data):
        """
        Creates a new Order instance based on validated data.
        """
        offer_details = OfferDetails.objects.get(pk=validated_data['offer_detail_id'])
        offer = offer_details.offer
        current_user = User.objects.get(pk=self.context['request'].user.pk)
        order = Order.objects.create(**get_order_create_dict(current_user, offer_details))
        return order
    
class CustomerReviewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for CustomerReview model with custom fields and methods for handling reviews.

    Attributes:
        reviewer (SerializerMethodField): Returns the reviewer's user ID.
        business_user (IntegerField): ID of the business user associated with the review.
    """
    reviewer = serializers.SerializerMethodField()
    business_user = serializers.IntegerField(required=False)
    
    class Meta:
        model = CustomerReview
        fields = ['id', 'reviewer', 'business_user', 'rating', 'description', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        """
        Modifies the representation to include the business user's ID.
        """
        representation = super().to_representation(instance)
        representation['business_user'] = instance.business_profile.user.pk if instance.business_profile else None
        return representation

    def get_reviewer(self, obj):
        return obj.reviewer_profile.user.pk
    
    def validate(self, attrs):
        """
        Validates required fields based on request method (POST or PATCH).
        """
        request = self.context.get('request')     
        if request and request.method == 'POST':
            validate_attrs_has_and_has_only_selected_fields(['business_user', 'rating', 'description'], attrs)
        elif request and request.method == 'PATCH':
            validate_attrs_has_only_selected_fields(['rating', 'description'], attrs)
        return attrs
    
    def create(self, validated_data):
        """
        Creates a new CustomerReview based on validated data.
        """
        current_user = User.objects.get(pk=self.context['request'].user.pk)
        business_user = validated_data.pop('business_user')
        review = CustomerReview.objects.create(
            reviewer_profile=CustomerProfile.objects.get(user=current_user),
            business_profile=BusinessProfile.objects.get(user=business_user),
            **validated_data,
        )
        return review