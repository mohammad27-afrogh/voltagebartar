from django.test import TestCase
from django.shortcuts import reverse

class TestBlogPageView(TestCase):
    def test_blog_page_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_blog_page_view_url_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_blog_page_view_content(self):
        response = self.client.get(reverse('blogs'))
        self.assertContains(response, 'blog page')

    def test_blog_page_view_template_used(self):
        response = self.client.get(reverse('blogs'))
        self.assertTemplateUsed(response, 'blogs/blog.html')
