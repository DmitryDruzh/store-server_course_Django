import stripe

from django.db import models
from django.conf import settings

from users.models import User

# Create your models here.
stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductsCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)
    stripe_product_price_id = models.CharField(max_length=28, null=True, blank=True)

    def __str__(self):
        return f'{self.name} | Категория: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(product=stripe_product['id'],
                                                   unit_amount=round(self.price * 100),  # in stripe_db 1000 = 10.00
                                                   currency='rub',
                                                   )
        return stripe_product_price

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for item in self:
            product_stripe_price = {
                    'price': item.product.stripe_product_price_id,
                    'quantity': item.quantity,
                }
            line_items.append(product_stripe_price)
        return line_items

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.sum())
        }
        return basket_item
