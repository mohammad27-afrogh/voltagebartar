from django.urls import path, re_path

from .views import (
    cart_detail_view,
    add_to_cart_view,
    remove_from_cart,
    clear_from_cart,
)

app_name = 'cart'

urlpatterns = [
    path('', cart_detail_view, name='Cart_detail'),
    re_path(r'^(?P<product_slug>[^/]+)/$', add_to_cart_view, name='cart_add'),
    re_path(r'^(?P<product_slug>[^/]+)/$', remove_from_cart, name='cart_remove'),
    path('clear/', clear_from_cart, name='cart_clear'),
]
