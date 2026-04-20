from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import AddToCartProductForm

def cart_detail_view(request):
    cart = Cart(request)

    cart_items_qith_forms = cart.get_items_with_forms()

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items_qith_forms,
    })

@require_POST
def add_to_cart_view(request, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])

    return redirect('cart:Cart_detail')

def remove_from_cart(request, product_slug):
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)
    cart.remove(product)

    return redirect('cart:Cart_detail')

def clear_from_cart(request):
    cart = Cart(request)

    cart.clear()

    return redirect('cart:Cart_detail')
