from django.urls import path, include

from .import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create_view, name='order_create'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_order/', views.profile_order_view, name='profile_order'),
    path('profile_favorites/', views.profile_favorites_view, name='profile_favorites'),
    path('profile_address/', views.profile_address_view, name='profile_address'),
    path('address/edit/', views.profile_address_edit_view, name='address_edit'),
    # path('address_delete/', views.remove_from_profile_address, name='remove_profile_address'),
    path('profile_comment/', views.profile_comment_view, name='profile_comment'),
    path('profile_create/', views.profile_user_create_view, name='profile_create'),
    path('profile/edit/', views.profile_user_edit_view, name='profile_user_edit'),
]
