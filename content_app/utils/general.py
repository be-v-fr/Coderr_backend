from django.db import IntegrityError
from rest_framework import status, serializers
from rest_framework.response import Response

def features_list_to_str(features_list):
    return ',,'.join(features_list)

def get_features_list_from_str(features_str):
    return features_str.split(',,') if features_str else []

def merge_features_keys(details_data):
    """
    By default, the DRF ListField serializer replaces the data key name with the source method name.
    In this case, the 'features' key is renamed to 'get_features_list'.
    This function serves as a workaround for this issue by undoing this action. 
    """
    if ('features' not in details_data) and ('get_features_list' in details_data):
        details_data['features'] = details_data.pop('get_features_list')
    return details_data

def get_offer_unique_error_details(error_msg):
    if 'content_app_offerdetails.offer_type' in error_msg:
        return {'details': 'Der Angebotstyp existiert für dieses Angebot bereits.'}
    elif 'content_app_offer.title' in error_msg:
        return {'title': 'Dieser Nutzer hat bereits ein Angebot mit diesem Titel.'}
    else:
        return {'error': 'Ein Angebot mit diesen Daten existiert bereits.'}
    
def get_integrity_error_response(error):
    error_msg = str(error)
    if 'UNIQUE constraint failed' in error_msg:
        custom_error_dict = get_offer_unique_error_details(error_msg)
        return Response(custom_error_dict, status=status.HTTP_409_CONFLICT)
    else:
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def update_offer(offer_view, offer_serializer):
    try:
        offer_serializer.is_valid(raise_exception=True)
        offer_view.perform_update(offer_serializer)
        return Response(offer_serializer.data, status=status.HTTP_200_OK)
    except IntegrityError as e:
        return get_integrity_error_response(e)
    except:
        return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
def validate_attrs_has_only_selected_fields(fields, attrs):
    for field in fields:
        if field not in attrs:
            raise serializers.ValidationError({field: "Dieses Feld wird benötigt."})
    
def validate_attrs_has_and_has_only_selected_fields(fields, attrs):
    validate_attrs_has_only_selected_fields(fields, attrs)
    for field in attrs.keys():
        if field not in attrs:
            raise serializers.ValidationError({field: "Dieses Feld ist für diese Anfrage nicht erlaubt."})
        
def get_order_create_dict(current_user, offer_details):
    return {
        'orderer_profile': current_user.customer_profile,
        'business_profile': offer_details.offer.business_profile,
        'title': offer_details.offer.title,
        'offer_details': offer_details,
        'price': offer_details.price,
        'features': offer_details.features,
        'revisions': offer_details.revisions,
        'delivery_time_in_days': offer_details.delivery_time_in_days,
    }