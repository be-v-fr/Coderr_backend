from rest_framework import serializers
from content_app.models import OfferDetails
from content_app.api.serializers.general import OfferDetailsSerializer
from .general import merge_features_keys, features_list_to_str

def create_offer_details(offer_id, data, context):
    """
    Creates a new `OfferDetails` instance associated with a specified offer.

    This function merges feature keys in the provided data, adds the offer ID to 
    the data, and uses the `OfferDetailsSerializer` to validate and save the new 
    offer details.

    Args:
        offer_id (int): The ID of the offer to associate with the new details.
        data (dict): The data to use for creating the offer details.
        context (dict): Additional context to pass to the serializer.

    Raises:
        serializers.ValidationError: If the data is invalid as per the serializer's validation rules.
    """
    data = merge_features_keys(data)
    data['offer_id'] = offer_id
    details_serializer = OfferDetailsSerializer(data=data, context=context)
    if details_serializer.is_valid(raise_exception=True):
        details_serializer.save()
        
def update_offer_details(offer, data):
    """
    Updates an existing `OfferDetails` instance or creates a new one if the specified offer type does not exist.

    This function merges feature keys in the data, verifies that an offer type is present, 
    and either updates an existing `OfferDetails` instance for the offer type or creates 
    a new one if none exists.

    Args:
        offer (Offer): The offer object to which the details belong.
        data (dict): The data to use for updating or creating the offer details.

    Raises:
        serializers.ValidationError: If the offer type is not specified in the data.
    """
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