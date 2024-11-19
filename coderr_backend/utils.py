from django.urls import reverse
from urllib.parse import urlencode

def format_number(value, decimal_places):
    """
    Formats number using a given number of decimal places.
    If the number itself has less decimal places, only one decimal place will show
    (e.g. 'format_number(7, 2)' returns '7.0' rather than '7.00').
    """
    return float(f"{value:.{decimal_places}f}")

def reverse_with_queryparams(view_name, *args, **kwargs):
    """
    Retrieves an API view URL combined with query parameters.
    """
    return reverse(view_name, args=args) + '?' + urlencode(kwargs)