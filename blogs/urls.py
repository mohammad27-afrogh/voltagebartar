from django.urls import path, include

from.views import blog_page_view, blog_detail_view

urlpatterns = [
    path('', blog_page_view, name='blogs'),
    path('<slug:blog_slug>/', blog_detail_view, name='blog_detail_by_slug'),
]