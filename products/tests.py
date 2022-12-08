from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from products.models import Product, ProductsCategory


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store | Home page')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories_01.json', 'products_01.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductsCategory.objects.first()
        path = reverse('category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store | Каталог')




