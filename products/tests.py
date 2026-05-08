from django.test import TestCase, Client
from django.shortcuts import reverse
from django.utils import timezone
from decimal import Decimal

from .models import Product, Category, Features


class ProductListViewTest(TestCase):
    def test_product_list_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_url_by_name(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_template_used(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertTemplateUsed((response, 'product_list.html'))


class ProductDetailViewTest(TestCase):
    def setUp(self):

        self.test_category = Category.objects.create(
            name = 'Test',
            slug = 'test',
        )

        self.test_features = Features.objects.create(
            name_features = 'Test_Standard',
            weight = Decimal('500.00'),
            weight_unit = 'GR',
        )

        self.test_product = Product.objects.create(
            name = 'product test 1',
            slug = 'product_test_1',
            sku = 'TEST_0012',
            category = self.test_category,
            features = self.test_features,
            base_price = Decimal('15000.00'),
            product_type = 'FER',
            commodity_status = 'AVA',
            short_description = 'a product test',
            description = 'a product test 1 to the Fertilizer',
        )
        self.client = Client()

    def test_product_detail_view_url_success(self):
        url = reverse('products:product_detail_by_slug', kwargs={
            'product_slug': self.test_product.slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.test_product.name)

    def test_product_detail_view_not_found(self):
        non_existent_slug = 'this_slug_dose_not_exist'
        url = reverse('products:product_detail_by_slug', kwargs={
            'product_slug': non_existent_slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)