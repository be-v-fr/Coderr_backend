def features_list_to_str(features_list):
    return ',,'.join(features_list)

def merge_features_keys(details_data):
    """
    By default, the DRF ListField serializer replaces the data key name with the source method name.
    In this case, the 'features' key is renamed to 'get_features_list'.
    This function serves as a workaround by undoing this action. 
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