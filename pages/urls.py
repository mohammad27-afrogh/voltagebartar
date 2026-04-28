from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('privacy/', views.PrivacyPageView.as_view(), name='privacy'),
    path('order_registration/', views.OrderRegistrationPageView.as_view(), name='order_registration'),
    path('faq/', views.faq_home_page_view, name='faq'),
    path('news/', views.news_room_page_view, name='news_room_page_view'),
    re_path(r'(?P<news_slug>[^/]+)/$', views.news_detail_by_slug, name='news_detail_by_slug'),
]
