from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BaseInfoSerializer
from content_app.models import Order
from statistics_app.utils import get_business_user_orders

class BaseInfoView(APIView):
             
    def get(self, request, *args, **kwargs):
        serializer = BaseInfoSerializer()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OrderCountView(APIView):
    def get(self, request, pk, format=None):
        orders = get_business_user_orders(pk)
        if orders:
            return Response({'order_count': orders.count()})
        return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)

    
class CompletedOrderCountView(APIView):
    def get(self, request, pk, format=None):
        orders = get_business_user_orders(pk)
        if orders:
            orders = orders.filter(status=Order.COMPLETED)
            return Response({'completed_order_count': orders.count()})
        return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)

