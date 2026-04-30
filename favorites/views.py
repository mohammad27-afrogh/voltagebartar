from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import FavoriteProduct
from products.models import Product
from orders.models import Profile


@login_required
def favorite_list_view(request):
    
    profile, created  = Profile.objects.get_or_create(user=request.user)

    favorite_list = FavoriteProduct.objects.filter(user=request.user).select_related('product')

    context = {
        'favorite_list': favorite_list,
        'profile': profile,
    }

    return render(request, 'orders/profile_favorite.html', context)


@login_required
@require_POST
def favorite_add_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    FavoriteProduct.objects.get_or_create(user=request.user, product=product)

# در اینجا باید حواسم باشه که ریدایرکت میکنم به خود صفحه product_detail 
# باید slug  رو برابر با همین صفحه بزارم (به همین صفحه با همین اسلاگ برگرد)
    return redirect('products:product_detail_by_slug', product_slug=product.slug)


@login_required
def favorite_delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    FavoriteProduct.objects.filter(user=request.user, product=product).delete()

    return redirect('favorite:favorite_list')

