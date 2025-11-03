from django.shortcuts import render
from django.views import generic

from .models import Blog

class BlogsHomePageView(generic.ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'blogs'
