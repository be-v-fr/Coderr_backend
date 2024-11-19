from rest_framework import serializers
from content_app.models import Offer, OfferDetails
from content_app.utils.general import features_list_to_str, merge_features_keys

class OfferDetailsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for OfferDetails model, with support for URL generation, feature validation, and custom handling
    of feature representation.

    Attributes:
        url (SerializerMethodField): Generates URL based on `obj.pk`.
        features (ListField): A list of feature strings, sourced from `get_features_list`.
        offer_id (IntegerField): Write-only field for Offer ID, allowing linkage on creation.
        offer_type (CharField): Required Offer type string.
        price (CharField): Required price string.
    """
    url = serializers.SerializerMethodField()
    features = serializers.ListField(
        child=serializers.CharField(max_length=31),
        source='get_features_list'
    )
    offer_id = serializers.IntegerField(write_only=True, required=False)
    offer_type = serializers.CharField(max_length=16, required=True)
    price = serializers.FloatField(required=True)

    class Meta:
        model = OfferDetails
        fields = ['id', 'offer_id', 'url', 'title', 'offer_type', 'price', 'features', 'revisions', 'delivery_time_in_days']
        
    def to_representation(self, instance):
        """
        Customizes the output fields based on the request path and method.
        """
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
        """
        Validates each feature in the `features` list to ensure it does not contain double commas.
        """
        if any(',,' in feature for feature in value):
            raise serializers.ValidationError('No double commas allowed.')
        return value
    
    def get_url(self, obj):
        """
        Generates a URL for the OfferDetails instance.
        """
        return f"/offerdetails/{obj.pk}/"

    def create(self, validated_data):
        """
        Creates a new OfferDetails instance linked to an Offer.
        """
        validated_data = merge_features_keys(validated_data)
        validated_data['features'] = features_list_to_str(validated_data['features'])
        offer_id = validated_data.pop('offer_id')
        offer = Offer.objects.get(pk=offer_id)
        instance = OfferDetails.objects.create(offer=offer, **validated_data)
        return instance
    
    def update(self, instance, validated_data):
        """
        Updates an existing OfferDetails instance with provided validated data.
        """
        validated_data = merge_features_keys(validated_data)
        validated_data['features'] = features_list_to_str(validated_data['features'])
        return super().update(instance, validated_data)