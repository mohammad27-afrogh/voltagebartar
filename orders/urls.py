from django.urls import path, include

from .import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create_view, name='order_create'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_order/', views.profile_orders_view, name='profile_order'),
    path('order_view/', views.profile_order_view, name='order_view'),
    path('profile_favorites/', views.profile_favorites_view, name='profile_favorites'),
    path('profile_address/', views.profile_address_view, name='profile_address'),
    path('address/edit/', views.profile_address_edit_view, name='address_edit'),
    path('profile_comment/', views.profile_comment_view, name='profile_comment'),
    path('comment_remove/<int:comment_id>/', views.profile_comment_remove, name='comment_remove'),
    path('profile/edit/', views.profile_user_edit_view, name='profile_user_edit'),
]
