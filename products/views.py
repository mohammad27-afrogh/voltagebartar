from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import  Product

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
    return render(request, 'products/product_detail.html',{
        'product': product_comment,
        'comments': product_comments,
    })
