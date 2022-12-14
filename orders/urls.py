from django.urls import path

from .views import *

urlpatterns = [
    path('', OrderListView.as_view(), name='orders_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),
    path('create', OrderCreateView.as_view(), name='order_create'),
    path('success', OrderSuccessView.as_view(), name='order_success'),
    path('canceled', CanceledTemplateView.as_view(), name='order_canceled')
]