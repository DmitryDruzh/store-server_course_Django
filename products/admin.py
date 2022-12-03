from django.contrib import admin
from .models import ProductsCategory, Product, Basket


# Register your models here.
admin.site.register(ProductsCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    fields = ('name', 'category', ('price', 'quantity'), 'image', 'description')
    search = ('name',)
    list_filter = ('category', )
    ordering = ('name',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 1
