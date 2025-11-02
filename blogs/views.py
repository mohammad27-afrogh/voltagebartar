from django.shortcuts import render

from django.views.generic import TemplateView

class BlogsHomePageView(TemplateView):
    template_name = 'blogs/blog.html'