from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('allauth.urls')),
    path('accounts/password/change/done/', views.password_change_done, name='account_password_change_done'),
]
