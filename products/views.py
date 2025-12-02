from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings

from .models import  Product, Comment, Category
from .forms import CommentForm

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

def product_detail_view(request, product_slug):
    product_comment = get_object_or_404(Product, slug=product_slug)
    product_comments = product_comment.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product_comment
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'products/product_detail.html', {
        'product': product_comment,
        'comments': product_comments,
        'comment_form': comment_form,
        'media_url': settings.MEDIA_URL,
    })

def category_detail_view(request, category_slug):
    current_category = get_object_or_404(Category, slug=category_slug)

    products_in_category = Product.objects.filter(category=current_category)

    context = {
        'category': current_category,
        'products': products_in_category,
    }

    return render(request, 'products/product_list.html', context)
