from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

import jdatetime
from .forms import OrderForm
from cart.cart import Cart
from .models import OrderItem, Order

@login_required
def order_create_view(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You cannot go to the order page. Please select your product from the store first.'))
        return redirect('cart:Cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order_obj = form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order = order_obj,
                    product = product,
                    quantity = item['quantity'],
                    price = product.base_price,
                )

            cart.clear()

    else:
        form = OrderForm()
    return render (request, 'orders/order_create.html', context={
        'form': form,
    })



@login_required
def profile_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    
    # 2. استخراج نام کاربری (Username) یا نام اصلی (First Name)
    # اگر نام کاربری را می‌خواهید:
    username = current_user.username

    
    # 1. گرفتن تاریخ میلادی
    gregorian_join_date = current_user.date_joined 
    
    # 2. تبدیل به شمسی (Jalali)
    # اگر date_joined از نوع None نباشد
    if gregorian_join_date:
        # تبدیل به آبجکت JalaliDate/JalaliDateTime
        jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        
        # تبدیل به رشته شمسی با فرمت دلخواه (مثلاً 1404/11/15)
        jalali_date_str = jalali_date.strftime("%Y/%m/%d") 
    else:
        jalali_date_str = "تاریخ نامشخص"

    # اگر نام و نام خانوادگی ثبت شده در مدل User را می‌خواهید:
    first_name = current_user.first_name
    last_name = current_user.last_name
    
    # 3. ارسال داده‌ها به قالب (Template)
    context = {
        'username': username,
        'jalali_date_str': jalali_date_str,
        'first_name': first_name,
        'last_name': last_name
    }
    
    return render(request, 'orders/profile_user.html', context)


@login_required
def profile_order_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    
    orders_whit_items = Order.objects.prefetch_related('items').all()

    context = {
        'orders_whit_items': orders_whit_items,
    }

    return render(request, 'orders/profile_order.html', context)


@login_required
def profile_favorites_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user

    orders = OrderItem.objects.prefetch_related('items').all()

    context = {
        'orders': orders,
    }

    return render(request, 'orders/profile_favorites.html', context)


@login_required
def profile_address_view(request):

    order_address = Order.objects.prefetch_related('items').all()

    context = {
        'order_address': order_address,
    }

    return render(request, 'orders/profile_address.html', context)


# @login_required
# def remove_from_profile_address(request, current_user):
#     address = OrderItem(request)

#     product = get_object_or_404(Order, slug=current_user)
#     address.remove(product)

#     return redirect('order:remove_profile_address')

@login_required
def profile_comment_view(request):

    return render(request, 'orders/profile_comment.html')

