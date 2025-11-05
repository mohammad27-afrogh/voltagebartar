from django.test import TestCase, Client
from django.shortcuts import reverse

from .models import Blog, Category

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

class TestBlogDetailView(TestCase):
    def setUp(self):

        self.test_category = Category.objects.create(
            name='TestBlog',
            slug='test_blog',
        )

        self.test_blog = Blog.objects.create(
            name = 'Blog_Test_1',
            slug = 'blog_test_1',
            category = self.test_category,
            short_description = 'test blog 1 this is a flower',
            description = 'test blog 1 this is a flower sanseveria',
        )
        self.client = Client()

    def test_blog_detail_view_url_success(self):
        url = reverse('blog_detail_by_slug', kwargs={
            'blog_slug': self.test_blog.slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.test_blog.name)
        self.assertContains(response, 'Blog_Test_1')

    def test_blog_detail_view_not_found(self):
        non_existent_slug = 'this_slug_dose_not_exist'
        url = reverse('blog_detail_by_slug', kwargs={
            'blog_slug': non_existent_slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)