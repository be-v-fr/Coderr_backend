from django.urls import path
from .views import BaseInfoView, OrderCountView, CompletedOrderCountView

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='base-info-list'),
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count-detail'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count-detail'),
]
