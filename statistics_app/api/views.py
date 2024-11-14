from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BaseInfoSerializer
from content_app.models import Order
from statistics_app.utils import get_business_user_orders

class BaseInfoView(APIView):
    """
    A view to retrieve general application statistics, including review count,
    average rating, business profile count, and offer count.
    """
    def get(self, request, *args, **kwargs):
        serializer = BaseInfoSerializer({})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderCountView(APIView):
    """
    A view to retrieve the count of orders with 'in progress' status for a specific business user.
    """
    def get(self, request, pk, format=None):
        try:
            orders = get_business_user_orders(pk)
        except:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
        orders = orders.filter(status=Order.IN_PROGRESS)
        return Response({'order_count': orders.count()})
    
class CompletedOrderCountView(APIView):
    """
    A view to retrieve the count of completed orders for a specific business user.
    """
    def get(self, request, pk, format=None):
        try:
            orders = get_business_user_orders(pk)
        except:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)
        orders = orders.filter(status=Order.COMPLETED)
        return Response({'completed_order_count': orders.count()})


