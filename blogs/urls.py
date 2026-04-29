from django.urls import path, re_path, include

from.views import blog_page_view, blog_detail_view

app_name='blog'

urlpatterns = [
    path('', blog_page_view, name='blogs'),
    re_path(r'^(?P<blog_slug>[^/]+)/$', blog_detail_view, name='blog_detail_by_slug'),
]