from django.db import IntegrityError
from rest_framework import status, serializers
from rest_framework.response import Response

def features_list_to_str(features_list):
    """
    Converts a list of features into a single string, with features separated by ',,'.

    Args:
        features_list (list): List of features to be converted.

    Returns:
        str: A single string of double-comma-separated features.
    """
    return ',,'.join(features_list)

def get_features_list_from_str(features_str):
    """
    Converts a comma-separated string of features back into a list.

    Args:
        features_str (str): String of features, separated by ',,'.

    Returns:
        list: A list of individual features.
    """
    return features_str.split(',,') if features_str else []

def merge_features_keys(details_data):
    """
    Adjusts the key name of 'features' if it was incorrectly set to 'get_features_list'
    by the Django REST Framework serializer.

    Args:
        details_data (dict): Dictionary containing offer details.

    Returns:
        dict: Dictionary with 'features' key corrected if necessary.
    """
    if ('features' not in details_data) and ('get_features_list' in details_data):
        details_data['features'] = details_data.pop('get_features_list')
    return details_data

def get_offer_unique_error_details(error_msg):
    """
    Determines a custom error message based on the integrity error type in an offer.

    Args:
        error_msg (str): The error message from the database.

    Returns:
        dict: Dictionary containing an appropriate error message.
    """
    if 'content_app_offerdetails.offer_type' in error_msg:
        return {'details': 'Der Angebotstyp existiert für dieses Angebot bereits.'}
    elif 'content_app_offer.title' in error_msg:
        return {'title': 'Dieser Nutzer hat bereits ein Angebot mit diesem Titel.'}
    else:
        return {'error': 'Ein Angebot mit diesen Daten existiert bereits.'}
    
def get_integrity_error_response(error):
    """
    Creates an appropriate HTTP response for a database integrity error.

    Args:
        error (IntegrityError): The integrity error exception raised.

    Returns:
        Response: HTTP response with appropriate status and error details.
    """
    error_msg = str(error)
    if 'UNIQUE constraint failed' in error_msg:
        custom_error_dict = get_offer_unique_error_details(error_msg)
        return Response(custom_error_dict, status=status.HTTP_409_CONFLICT)
    else:
        return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def update_offer(offer_view, offer_serializer):
    """
    Attempts to update an offer using the provided serializer and view, handling any integrity errors.

    Args:
        offer_view (View): The view handling the update.
        offer_serializer (Serializer): The serializer containing the update data.

    Returns:
        Response: HTTP response with the result of the update.
    """
    try:
        offer_serializer.is_valid(raise_exception=True)
        offer_view.perform_update(offer_serializer)
        return Response(offer_serializer.data, status=status.HTTP_200_OK)
    except IntegrityError as e:
        return get_integrity_error_response(e)
    except:
        return Response(offer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
def validate_attrs_has_only_selected_fields(fields, attrs):
    """
    Validates that only the specified fields are present in the attributes.

    Args:
        fields (list): List of allowed field names.
        attrs (dict): Attributes dictionary to validate.

    Raises:
        ValidationError: If a required field is missing.
    """
    for field in fields:
        if field not in attrs:
            raise serializers.ValidationError({field: "This field is required."})
    
def validate_attrs_has_and_has_only_selected_fields(fields, attrs):
    """
    Validates that only the specified fields are present and that none are missing.

    Args:
        fields (list): List of allowed field names.
        attrs (dict): Attributes dictionary to validate.

    Raises:
        ValidationError: If a field is missing or an extra field is present.
    """
    validate_attrs_has_only_selected_fields(fields, attrs)
    for field in attrs.keys():
        if field not in attrs:
            raise serializers.ValidationError({field: "This field is not allowed for this request."})
        
def get_order_create_dict(current_user, offer_details):
    """
    Creates a dictionary for an order based on the current user and offer details.

    Args:
        current_user (User): The user creating the order.
        offer_details (OfferDetails): The details of the offer.

    Returns:
        dict: Dictionary containing order data.
    """
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