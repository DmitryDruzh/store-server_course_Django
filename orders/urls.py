from django.urls import path

from .views import *

urlpatterns = [
    path('create', OrderCreateView.as_view(), name='order_create'),
    path('success', OrderSuccessView.as_view(), name='order_success'),
]