from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Blog
from .forms import CommentForm

class BlogsHomePageView(generic.ListView):
    model = Blog
    template_name = 'blogs/blog.html'
    context_object_name = 'blogs'

def blog_detail_view(request, blog_slug):
    blog_comment = get_object_or_404(Blog, slug=blog_slug)
    blog_comments = blog_comment.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog_comment
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog_comment,
        'comments': blog_comments,
        'comment_form': comment_form,
    })