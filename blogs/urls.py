from django.urls import path, include

from.views import BlogsHomePageView

urlpatterns = [
    path('', BlogsHomePageView.as_view(), name='blogs'),
]