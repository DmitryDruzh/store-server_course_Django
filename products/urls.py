from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductsListView.as_view(), name='products'),
    path('category/<category_id>', ProductsListView.as_view(), name='category'),
    path('page/<int:page>', ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:product_id>', basket_add, name='basket_add'),
    path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove')
]