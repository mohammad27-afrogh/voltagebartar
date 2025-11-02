from django.test import TestCase
from django.shortcuts import reverse

class HomePageViewTest(TestCase):
    def test_home_page_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_url_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'home page')

    def test_home_page_view_template_used(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed((response, 'home.html'))

class AboutUsPageViewTest(TestCase):
    def test_about_us_page_view_url(self):
        response = self.client.get('/aboutus/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_view_url_by_name(self):
        response = self.client.get(reverse('aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_view_content(self):
        response = self.client.get(reverse('aboutus'))
        self.assertContains(response, 'about us')

    def test_about_us_page_view_template_used(self):
        response = self.client.get(reverse('aboutus'))
        self.assertTemplateUsed((response, 'aboutus.html'))