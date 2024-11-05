from django.db import IntegrityError
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from users_app.api.permissions import ReadOnly, PostAsBusinessUser, PostAsCustomerUser
from content_app.utils import get_integrity_error_response
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from .serializers import OfferSerializer, OfferDetailsSerializer, OrderSerializer, CustomerReviewSerializer
from .filters import OfferFilter
from .pagination import OfferPagination
from .permissions import PatchAsCreator, PatchAsReviewer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().annotate(min_price=Min('details__price'))
    serializer_class = OfferSerializer
    permission_classes = [PostAsBusinessUser|PatchAsCreator|ReadOnly]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return get_integrity_error_response(e)
            
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return get_integrity_error_response(e)
    
class OfferDetailsViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [ReadOnly] # OfferDetails changes are communicated via OfferViewSet PATCH requests
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [PostAsCustomerUser|PatchAsCreator|ReadOnly]
    
class CustomerReviewViewSet(viewsets.ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [PostAsCustomerUser|PatchAsReviewer|ReadOnly]