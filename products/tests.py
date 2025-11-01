from django.test import TestCase
from django.shortcuts import reverse


class ProductListViewTest(TestCase):
    def test_product_list_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_product_list_view_url_by_name(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_content(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, 'product list')

    def test_product_list_template_used(self):
        response = self.client.get(reverse('product_list'))
        self.assertTemplateUsed((response, 'product_list.html'))