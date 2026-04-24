from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

from .models import Blog
from .forms import CommentForm

def blog_page_view(request):
    blog = Blog.objects.all()

    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=60)

    latest_blog = blog.filter(Q(date_time_create__gte=one_month_ago) & Q(date_time_create__lte=default_time))

    return render(request, 'blogs/blog.html', context={
        'blog': blog,
        'latest_blog': latest_blog,
    })


def blog_detail_view(request, blog_slug):
    blog = Blog.objects.all()

    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=60)

    latest_blog = blog.filter(Q(date_time_create__gte=one_month_ago) & Q(date_time_create__lte=default_time))

    blog_detail = get_object_or_404(Blog, slug=blog_slug)
    blog_detail.view_count += 1
    blog_detail.save()

    blog_comments = blog_detail.comments.all()
    total_comment = len(blog_comments)
    # --- ۲. محاسبه زنجیره Breadcrumb در View ---
    category = blog_detail.category
    categories_chain = []

    if category:
        # اضافه کردن دسته فعلی
        categories_chain.append(category)

        # پیمایش به سمت بالا تا رسیدن به ریشه (category.parent = None)
        while category.parent_category:
            category = category.parent_category
            categories_chain.insert(0, category)  # اضافه کردن به ابتدای لیست


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blog = blog_detail
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'blogs/blog_detail.html', {
        'blog': blog_detail,
        'comments': blog_comments,
        'total_comment': total_comment,
        'comment_form': comment_form,
        'categories_chain': categories_chain,
        'latest_blog': latest_blog,
    })