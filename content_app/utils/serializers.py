from rest_framework import serializers
from content_app.models import OfferDetails
from content_app.api.serializers.general import OfferDetailsSerializer
from .general import merge_features_keys, features_list_to_str

def create_offer_details(offer_id, data, context):
    data = merge_features_keys(data)
    data['offer_id'] = offer_id
    details_serializer = OfferDetailsSerializer(data=data, context=context)
    if details_serializer.is_valid(raise_exception=True):
        details_serializer.save()
        
def update_offer_details(offer, data):
    data = merge_features_keys(data)
    offer_type = data.get('offer_type')
    if not offer_type:
        raise serializers.ValidationError('Offer details are missing an offer type.')
    details_instance = offer.details.filter(offer_type=offer_type).first()          
    if details_instance:
        for attr, value in data.items():
            if attr == 'features':
                value = features_list_to_str(value)
            setattr(details_instance, attr, value)
        details_instance.save()
    else:
        OfferDetails.objects.create(offer=offer, **data)