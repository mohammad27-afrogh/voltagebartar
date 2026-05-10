from django.urls import path, re_path, include

from .views import product_list_view, product_detail_view, category_detail_view

app_name = 'products'

urlpatterns = [
    path('', product_list_view, name='product_list'),
    re_path(r'(?P<product_slug>[^/]+)/$', product_detail_view, name='product_detail_by_slug'),
    re_path(r'^category/(?P<category_slug>[^/]+)/$', category_detail_view, name='category_detail'),
]