from django.urls import path, include

from.views import BlogsHomePageView, blog_detail_view

urlpatterns = [
    path('', BlogsHomePageView.as_view(), name='blogs'),
    path('<slug:blog_slug>/', blog_detail_view, name='blog_detail_by_slug'),
]