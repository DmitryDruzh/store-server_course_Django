from rest_framework import fields, serializers

from products.models import Basket, Product, ProductsCategory


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductsCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image', 'category')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=True)
    total_price = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()


    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_price', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_price(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_price()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()