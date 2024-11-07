from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import BusinessProfile, CustomerProfile
from users_app.api.serializers import UserSerializer
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from content_app.utils import features_list_to_str, merge_features_keys, get_order_create_dict
from content_app.utils import validate_attrs_has_only_selected_fields, validate_attrs_has_and_has_only_selected_fields

class OfferDetailsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    features = serializers.ListField(
        child=serializers.CharField(max_length=31),
        source='get_features_list'
    )
    offer_id = serializers.IntegerField(write_only=True, required=False)
    offer_type = serializers.CharField(max_length=16, required=True)
    price = serializers.CharField(max_length=8, required=True)

    class Meta:
        model = OfferDetails
        fields = ['id', 'offer_id', 'url', 'title', 'offer_type', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def to_representation(self, instance):
        request = self.context.get('request', None)
        if request:
            if 'offers' in request.path and request.method == 'GET':
                allowed_fields = {'id', 'url'}
                existing_fields = set(self.fields.keys())
                for field_name in existing_fields - allowed_fields:
                    self.fields.pop(field_name)
            else:
                self.fields.pop('url', None)
        return super().to_representation(instance)
        
    def validate_features(self, value):
        if any(',,' in feature for feature in value):
            raise serializers.ValidationError("Features dürfen kein Doppelkomma enthalten.")
        return value
    
    def get_url(self, obj):
        return f"/offerdetails/{obj.pk}/"

    def create(self, validated_data):
        validated_data = merge_features_keys(validated_data)
        validated_data['features'] = features_list_to_str(validated_data['features'])
        offer_id = validated_data.pop('offer_id')
        offer = Offer.objects.get(pk=offer_id)
        instance = OfferDetails.objects.create(offer=offer, **validated_data)
        return instance
    
    def update(self, instance, validated_data):
        validated_data = merge_features_keys(validated_data)
        validated_data['features'] = features_list_to_str(validated_data['features'])
        return super().update(instance, validated_data)

class OfferSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField()
    details = OfferDetailsSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
        
    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'description', 'image', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        
    def to_representation(self, instance):
        self.fields['details'].context.update(self.context)
        return super().to_representation(instance)
        
    def get_user(self, obj):
        return obj.business_profile.user.pk
    
    def get_min_price(self, obj):
        return obj.details.order_by('price_cents').first().price if obj.details.exists() else None
    
    def get_min_delivery_time(self, obj):
        return obj.details.order_by('delivery_time_in_days').first().delivery_time_in_days if obj.details.exists() else None
    
    def validate_details(self, value):
        offer_types = set()
        for detail in value:
            offer_type = detail.get('offer_type')
            if offer_type in offer_types:
                raise serializers.ValidationError('Jeder Angebotstyp darf nur einmal vorkommen.')
            offer_types.add(offer_type)  
        return value
    
    def create(self, validated_data):
        many_details_data = validated_data.pop('details', {})
        user = User.objects.get(pk=self.context['request'].user.pk)
        profile = BusinessProfile.objects.get(user=user)
        new_offer = Offer.objects.create(business_profile=profile, **validated_data)
        for single_details_data in many_details_data:
            single_details_data = merge_features_keys(single_details_data)
            single_details_data['offer_id'] = new_offer.pk
            details_serializer = OfferDetailsSerializer(data=single_details_data, context=self.context)
            if details_serializer.is_valid(raise_exception=True):
                details_serializer.save()
        return new_offer
        
    def update(self, instance, validated_data):
        many_details_data = validated_data.pop('details', {})
        updated_offer = super().update(instance, validated_data)
        for single_details_data in many_details_data:
            single_details_data = merge_features_keys(single_details_data)
            offer_type = single_details_data.get('offer_type', None)
            if offer_type:
                details_instance = instance.details.get(offer_type=offer_type)
                if details_instance:
                    details_serializer = OfferDetailsSerializer(data=single_details_data, instance=details_instance)
                else:
                    details_serializer = OfferDetailsSerializer(data=single_details_data, context=self.context)
                if details_serializer.is_valid():
                    details_serializer.save()
            else:
                raise serializers.ValidationError('Angebotstyp nicht spezifiziert.')
        return updated_offer
    
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_user = serializers.SerializerMethodField()
    business_user = serializers.SerializerMethodField()
    offer_detail_id = serializers.IntegerField(write_only=True)
    offer_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'status', 'offer_detail_id', 'offer_type', 'created_at', 'updated_at', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def get_customer_user(self, obj):
        return obj.orderer_profile.user.pk
    
    def get_business_user(self, obj):
        return obj.business_profile.user.pk
    
    def get_offer_type(self, obj):
        return obj.offer_details.offer_type
    
    def validate(self, attrs):
        request = self.context.get('request')     
        if request and request.method == 'POST':
            validate_attrs_has_and_has_only_selected_fields(['offer_detail_id'], attrs)
        elif request and request.method == 'PATCH':
            validate_attrs_has_and_has_only_selected_fields(['status'], attrs)
        return attrs

    def create(self, validated_data):
        offer_details = OfferDetails.objects.get(pk=validated_data['offer_detail_id'])
        offer = offer_details.offer
        current_user = User.objects.get(pk=self.context['request'].user.pk)
        order = Order.objects.create(**get_order_create_dict(current_user, offer_details))
        return order
    
class CustomerReviewSerializer(serializers.HyperlinkedModelSerializer):
    reviewer = serializers.SerializerMethodField()
    business_user = serializers.IntegerField(required=False)
    
    class Meta:
        model = CustomerReview
        fields = ['id', 'reviewer', 'business_user', 'rating', 'description', 'created_at', 'updated_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['business_user'] = instance.business_profile.user.pk if instance.business_profile else None
        return representation

    def get_reviewer(self, obj):
        return obj.reviewer_profile.user.pk
    
    def validate(self, attrs):
        request = self.context.get('request')     
        if request and request.method == 'POST':
            validate_attrs_has_and_has_only_selected_fields(['business_user', 'rating', 'description'], attrs)
        elif request and request.method == 'PATCH':
            validate_attrs_has_only_selected_fields(['rating', 'description'], attrs)
        return attrs
    
    def create(self, validated_data):
        current_user = User.objects.get(pk=self.context['request'].user.pk)
        business_user = validated_data.pop('business_user')
        review = CustomerReview.objects.create(
            reviewer_profile=CustomerProfile.objects.get(user=current_user),
            business_profile=BusinessProfile.objects.get(user=business_user),
            **validated_data,
        )
        return review