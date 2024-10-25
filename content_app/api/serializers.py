from rest_framework import serializers
from users_app.api.serializers import BusinessProfileSerializer
from content_app.models import Offer, OfferDetails

class OfferSerializer(serializers.HyperlinkedModelSerializer):
    business_user = BusinessProfileSerializer()
    
    class Meta:
        model = Offer
        fields = ['business_user', 'description', 'image', 'created_at', 'created_at', 'min_price', 'min_delivery_time']
        
class OfferDetailsSerializer(serializers.HyperlinkedModelSerializer):
    offer = OfferSerializer()
    features = serializers.ListField(
        child=serializers.CharField(max_length=63),
        source='get_features_list',
    )

    class Meta:
        model = OfferDetails
        fields = ['offer_type', 'offer', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def validate_features(self, value):
        if any(',,' in feature for feature in value):
            raise serializers.ValidationError("Features dürfen kein Doppelkomma enthalten.")
        return value

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