from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import  Product, Comment
from .forms import CommentForm

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

# class ProductDetailView(generic.DetailView):
#     model = Product
#     template_name = 'products/product_detail.html'
#     context_object_name = 'product'
#     slug_field = 'slug'
#     slug_url_kwarg = 'product_slug'

def product_detail_view(request, product_slug):
    product_comment = get_object_or_404(Product, slug=product_slug)
    product_comments = product_comment.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product_comment = product_comment
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'products/product_detail.html', {
        'product': product_comment,
        'comments': product_comments,
        'comment_form': comment_form,
    })