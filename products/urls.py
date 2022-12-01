from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('products', products, name='products'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove')
]