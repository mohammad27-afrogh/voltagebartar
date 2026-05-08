from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from .models import NewsRoom

class HomePageViewTest(TestCase):
    def test_home_page_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_url_by_name(self):
        response = self.client.get(reverse('page:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_view_template_used(self):
        response = self.client.get(reverse('page:home'))
        self.assertTemplateUsed((response, 'home.html'))

class AboutUsPageViewTest(TestCase):
    def test_about_us_page_view_url(self):
        response = self.client.get('/aboutus/')
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_view_url_by_name(self):
        response = self.client.get(reverse('page:aboutus'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_page_view_template_used(self):
        response = self.client.get(reverse('page:aboutus'))
        self.assertTemplateUsed((response, 'aboutus.html'))


class PrivacyPageViewTest(TestCase):
    def test_privacy_page_view_url(self):
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_page_view_url_by_name(self):
        response = self.client.get(reverse('page:privacy'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_page_view_template_used(self):
        response = self.client.get(reverse('page:privacy'))
        self.assertTemplateUsed((response, 'privacy.html'))


class OrderRegistrationPageViewTest(TestCase):
    def test_order_registration_page_view_url(self):
        response = self.client.get('/order_registration/')
        self.assertEqual(response.status_code, 200)

    def test_order_registration_page_view_url_by_name(self):
        response = self.client.get(reverse('page:order_registration'))
        self.assertEqual(response.status_code, 200)

    def test_order_registration_page_view_template_used(self):
        response = self.client.get(reverse('page:order_registration'))
        self.assertTemplateUsed((response, 'order_registration.html'))


class FaqHomePageViewTest(TestCase):
    def test_faq_page_view_url(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)

    def test_faq_page_view_url_by_name(self):
        response = self.client.get(reverse('page:faq'))
        self.assertEqual(response.status_code, 200)

    def test_faq_page_view_template_used(self):
        response = self.client.get(reverse('page:faq'))
        self.assertTemplateUsed((response, 'faq.html'))


class NewsRoomPageViewTest(TestCase):
    def test_news_page_view_url(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_news_page_view_url_by_name(self):
        response = self.client.get(reverse('page:news_room_page_view'))
        self.assertEqual(response.status_code, 200)

    def test_news_room_page_view_page_view_template_used(self):
        response = self.client.get(reverse('page:news_room_page_view'))
        self.assertTemplateUsed((response, 'news_list.html'))



class TestNewsDetailView(TestCase):
    def setUp(self):

        User = get_user_model()
        self.user = User.objects.create_user(
                username = 'testernews',
                password = 'password123456',
                email = 'usernews@test.com'
            )

        self.test_news = NewsRoom.objects.create(
            admin = self.user,
            title = 'News_Room_1',
            slug = 'News_Room_1',
            category = 'ANN',
            short_description = 'test news room 1 this is a flower',
            description = 'test news rom 1 this is a flower sanseveria',
        )
        self.client = Client()

    def test_news_detail_view_url_success(self):
        url = reverse('page:news_detail_by_slug', kwargs={
            'news_slug': self.test_news.slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.test_news.title)
        self.assertContains(response, 'News_Room_1')

    def test_news_detail_view_not_found(self):
        non_existent_slug = 'this_slug_dose_not_exist'
        url = reverse('page:news_detail_by_slug', kwargs={
            'news_slug': non_existent_slug
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
