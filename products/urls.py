from django.urls import path, include

from .views import product_list_view, product_detail_view, category_detail_view

urlpatterns = [
    # path('', ProductListView.as_view(), name='product_list'),
    path('', product_list_view, name='product_list'),
    path('<slug:product_slug>/', product_detail_view, name='product_detail_by_slug'),
    path('category/<slug:category_slug>/', category_detail_view, name='category_detail'),
]