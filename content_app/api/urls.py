from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfferViewSet, OfferDetailsViewSet, OrderViewSet, CustomerReviewViewSet

router = DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')
router.register(r'offerdetails', OfferDetailsViewSet, basename='offerdetails')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'reviews', CustomerReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]