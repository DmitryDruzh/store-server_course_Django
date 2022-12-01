from django.shortcuts import render, HttpResponseRedirect
from .models import Product, ProductsCategory, Basket

from users.models import User

# Create your views here.


def index(request):

    return render(request, 'products/index.html')


def products(request):
    context = {
        'products': Product.objects.all(),
        'categories': ProductsCategory.objects.all()
    }
    return render(request, 'products/products.html', context)


def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)
    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = Basket.objects.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
