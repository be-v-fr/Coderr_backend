from rest_framework import serializers
from users_app.api.serializers import BusinessProfileSerializer
from content_app.models import Offer, OfferDetails

class OfferDetailsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    features = serializers.ListField(
        child=serializers.CharField(max_length=63),
        source='get_features_list',
    )

    class Meta:
        model = OfferDetails
        fields = ['id', 'url', 'offer_type', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
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

    def update(self, instance, validated_data):
        if 'features' in validated_data:
            instance.set_features_list(validated_data.pop('features'))
        return super().update(instance, validated_data)

    def create(self, validated_data):
        features = validated_data.pop('features', [])
        instance = OfferDetails(**validated_data)
        instance.set_features_list(features)
        instance.save()
        return instance

class OfferSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SerializerMethodField()
    details = OfferDetailsSerializer(many=True, source='get_details')
        
    class Meta:
        model = Offer
        fields = ['id', 'user', 'description', 'image', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        
    def to_representation(self, instance):
        self.fields['details'].context.update(self.context)
        return super().to_representation(instance)
        
    def get_user(self, obj):
        return obj.business_profile.user.pk