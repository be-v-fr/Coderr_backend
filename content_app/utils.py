from rest_framework import status
from rest_framework.response import Response

def features_list_to_str(features_list):
    return ',,'.join(features_list)

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