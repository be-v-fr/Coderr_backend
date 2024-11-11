from django.db import IntegrityError
from django.db.models import Min, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from users_app.api.permissions import ReadOnly, PostAsBusinessUser, PostAsCustomerUser
from uploads_app.utils import handle_file_update
from content_app.utils import get_integrity_error_response, update_offer
from content_app.models import Offer, OfferDetails, Order, CustomerReview
from .serializers import OfferSerializer, OfferDetailsSerializer, OrderSerializer, CustomerReviewSerializer
from .filters import OfferFilter, CustomerReviewFilter
from .pagination import OfferPagination
from .permissions import IsAdmin, IsCreator, PatchAsCreator, IsReviewer

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().annotate(min_price=Min('details__price_cents'))
    serializer_class = OfferSerializer
    permission_classes = [PostAsBusinessUser|IsCreator|ReadOnly]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
        upload_error = handle_file_update(obj=instance, data_dict=request.data, file_key='image')
        if upload_error:
            return Response(upload_error, status=status.HTTP_400_BAD_REQUEST)
        offer_serializer = self.get_serializer(instance, data=request.data, partial=partial)
        return update_offer(offer_view=self, offer_serializer=offer_serializer)
    
class OfferDetailsViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [ReadOnly] # OfferDetails are written via OfferViewSet PATCH requests
    
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [PostAsCustomerUser|PatchAsCreator|IsAdmin|ReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        return Order.objects.filter(
            Q(business_profile__user=user) | Q(orderer_profile__user=user)
        )
    
class CustomerReviewViewSet(viewsets.ModelViewSet):
    queryset = CustomerReview.objects.all()
    serializer_class = CustomerReviewSerializer
    permission_classes = [PostAsCustomerUser|IsReviewer|IsAdmin|ReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomerReviewFilter
    ordering_fields = ['updated_at', 'rating']