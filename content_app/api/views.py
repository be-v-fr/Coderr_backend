from django.db import IntegrityError
from rest_framework import status, viewsets, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from content_app.utils import get_offer_unique_error_details
from content_app.models import Offer, OfferDetails
from .serializers import OfferSerializer, OfferDetailsSerializer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            error_msg = str(e)
            if 'UNIQUE constraint failed' in error_msg:
                custom_error_dict = get_offer_unique_error_details(error_msg)
                return Response(custom_error_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': error_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class OfferDetailsViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer