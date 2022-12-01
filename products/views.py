from django.shortcuts import render
from .models import Product, ProductsCategory

# Create your views here.


def index(request):

    return render(request, 'products/index.html')


def products(request):
    context = {
        'products': Product.objects.all(),
        'categories': ProductsCategory.objects.all()
    }
    return render(request, 'products/products.html', context)