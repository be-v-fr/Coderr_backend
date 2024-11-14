from rest_framework import pagination

class OfferPagination(pagination.PageNumberPagination):
    """
    Custom pagination class for paginating offer results.

    Attributes:
        page_size (int): Default number of results per page. Defaults to 6.
        page_size_query_param (str): Query parameter name for specifying the 
            number of results per page. Defaults to 'page_size'.
        max_page_size (int): Maximum number of results allowed per page. Defaults to 60.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 60