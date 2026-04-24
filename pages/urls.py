from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('privacy/', views.PrivacyPageView.as_view(), name='privacy'),
    path('order_registration/', views.OrderRegistrationPageView.as_view(), name='order_registration'),
    path('faq/', views.faq_home_page_view, name='faq'),
]
