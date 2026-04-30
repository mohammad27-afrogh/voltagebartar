from django.urls import path

from . import views

app_name='favorite'

urlpatterns = [
    path('', views.favorite_list_view, name='favorite_list'),
    path('add/<int:product_id>/', views.favorite_add_view, name='favorite_add'),
    path('delete/<int:product_id>/', views.favorite_delete_view, name='favorite_delete'),
]
