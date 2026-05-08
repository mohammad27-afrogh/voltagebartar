from django.test import TestCase
from django.shortcuts import reverse

class TestCartDetailView(TestCase):
    def test_cart_detail_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_view_url_by_name(self):
        response = self.client.get(reverse('cart:Cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_view_template_used(self):
        response = self.client.get(reverse('cart:Cart_detail'))
        self.assertTemplateUsed(response, 'cart/cart_detail.html')