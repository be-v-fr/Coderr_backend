from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import BusinessProfile
from users_app.api.serializers import BusinessProfileSerializer
from content_app.models import Offer, OfferDetails
from content_app.utils import features_list_to_str

class OfferDetailsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    features = serializers.ListField(
        child=serializers.CharField(max_length=31),
        source='get_features_list'
    )
    offer_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = OfferDetails
        fields = ['id', 'offer_id', 'url', 'title', 'offer_type', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def to_representation(self, instance):
        request = self.context.get('request', None)
        if request:
            if request.method == 'GET':
                allowed_fields = {'id', 'url'}
                existing_fields = set(self.fields.keys())
                for field_name in existing_fields - allowed_fields:
                    self.fields.pop(field_name)
            elif request.method == 'POST':
                self.fields.pop('url', None)
        return super().to_representation(instance)
        
    def validate_features(self, value):
        if any(',,' in feature for feature in value):
            raise serializers.ValidationError("Features dürfen kein Doppelkomma enthalten.")
        return value
    
    def get_url(self, obj):
        return f"/offerdetails/{obj.pk}/"

    def create(self, validated_data):
        if ('features' not in validated_data) and ('get_features_list' in validated_data):
            validated_data['features'] = validated_data.pop('get_features_list')
        validated_data['features'] = features_list_to_str(validated_data['features'])
        offer_id = validated_data.pop('offer_id')
        offer = Offer.objects.get(pk=offer_id)
        object = OfferDetails.objects.create(offer=offer, **validated_data)
        return object

    def update(self, instance, validated_data):
        if ('features' not in validated_data) and ('get_features_list' in validated_data):
            validated_data['features'] = validated_data.pop('get_features_list')
        features_list = validated_data.pop('features', '')
        instance = super().update(instance, validated_data)
        if len(features_list) > 0:
            instance.set_features_str(features_list)
        instance.save()
        return instance

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
        return obj.details.order_by('price').first().price if obj.details.exists() else None
    
    def get_min_delivery_time(self, obj):
        return obj.details.order_by('delivery_time_in_days').first().delivery_time_in_days if obj.details.exists() else None
    
    def create(self, validated_data):
        many_details_data = validated_data.pop('details', {})
        user = User.objects.get(pk=self.context['request'].user.pk)
        profile = BusinessProfile.objects.get(user=user)
        new_offer = Offer.objects.create(business_profile=profile, **validated_data)
        for single_details_data in many_details_data:
            if ('features' not in single_details_data) and ('get_features_list' in single_details_data):
                single_details_data['features'] = single_details_data.pop('get_features_list')
            single_details_data['offer_id'] = new_offer.pk
            details_serializer = OfferDetailsSerializer(data=single_details_data, context=self.context)
            if details_serializer.is_valid(raise_exception=True):
                details_serializer.save()
        return new_offer
        