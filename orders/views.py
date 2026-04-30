from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import jdatetime
from .forms import AddressFormOrder, ProfileFormBasic, ProfileFormLocations
from cart.cart import Cart
from products.models import Comment, Product
from .models import OrderItem, Order, Profile


@login_required
def order_create_view(request):
    cart = Cart(request)
    cart_items = list(cart.get_items_with_forms())

    if len(cart) == 0:
        messages.warning(request, _('You cannot go to the order page. Please select your product from the store first.'))
        return redirect('cart:Cart_detail')

    if request.method == 'POST':
        form = AddressFormOrder(request.POST)
        if form.is_valid():
            order_obj = form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart_items:
                product = item.get('product_obj')
                quantity = item.get('quantity')

                if product and quantity is not None:
                    order_item, created = OrderItem.objects.get_or_create(
                        order = order_obj,
                        product = product,
                        quantity = quantity,
                        price = product.base_price
                    )

                    if created:
                        order_item.quantity = quantity
                        order_item.price = product.base_price
                    else:
                        order_item.quantity += quantity
                    
                    order_item.save()

            cart.clear()

            if order_obj.pyment_price == 'HD':
                order_item = order_obj.items.select_related('product').all()

                order_obj.status = 'PEN'
                order_obj.is_paid = False
                order_obj.save()

                for item in order_item:
                    if item.product:
                        item.product.successful_sales_count = F('successful_sales_count') + item.quantity
                        item.product.save(update_fields=['successful_sales_count'])
                

                return render(request, 'cart/cart_checkout_complete_buy.html', context={
                    'order_obj': order_obj,
                })
            else:
                request.session['order_id'] = order_obj.id
                return redirect('payment_process')

    else:
        form = AddressFormOrder()
    return render (request, 'cart/cart_checkout.html', context={
        'cart_items': cart_items,
        'form': form,
    })


@login_required
def profile_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    profile, created  = Profile.objects.get_or_create(user=current_user)
    username = current_user

    incomplete_fields = []
    if not profile.first_name:
        incomplete_fields.append(_('first_name'))
    if not profile.last_name:
        incomplete_fields.append(_('last_name'))
    if not profile.phone_number:
        incomplete_fields.append(_('phone_number'))
    if not profile.national_number:
        incomplete_fields.append(_('national_number'))
    if not profile.Receive_the_newsletter:
        incomplete_fields.append(_('Receive_the_newsletter'))
    if not profile.email:
        incomplete_fields.append(_('email'))

    # 3. ارسال داده‌ها به قالب (Template)
    context = {
        'username': username,
        'profile': profile,
        'incomplete_fields': incomplete_fields,
    }
    
    return render(request, 'orders/profile_user.html', context)


@login_required
def profile_user_edit_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    if request.method == 'POST':
        form = ProfileFormBasic(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('order:profile'))
    else:
        form = ProfileFormBasic(instance=profile)

    context = {
        'profile': profile,
        'username': username,
        'form': form,
    }

    return render(request, 'orders/profile_user_edit.html', context)


@login_required
def profile_orders_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)
    
    orders_whit_items = Order.objects.filter(user=current_user).prefetch_related('items').all()

    context = {
        'username': username,
        'profile': profile,
        'orders_whit_items': orders_whit_items,
    }

    return render(request, 'orders/profile_order.html', context)


@login_required
def profile_order_view(request):
    current_user = request.user
    username = current_user
    # 1. پیدا کردن شیء ORDER تکی با استفاده از get_object_or_404
    # این شیء تکی (object) دارای فیلدهای آدرس است.
    # ما از select_related برای بهینه‌سازی دسترسی به آدرس‌ها استفاده می‌کنیم.

    order = get_object_or_404(Order, user=current_user)

    profile, created  = Profile.objects.get_or_create(user=current_user)

    order_items_product = order.items.select_related('product').all()

    total_order_item = 0

    for item in order_items_product:
        item_product_price = item.quantity * item.price

    total_order_item = item_product_price + total_order_item

    context = {
        'username': username,
        'profile': profile,
        'order': order,
        'order_items_product': order_items_product,
        'item_product_price': item_product_price,
        'total_order_item': total_order_item,
    }

    return render(request, 'orders/profile_order_view.html', context)


@login_required
def profile_address_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    incomplete_fields_address = []
    if not profile.phone_number:
        incomplete_fields_address.append(_('phone_number'))
    if not profile.province_address:
        incomplete_fields_address.append(_('province_address'))
    if not profile.city_address:
        incomplete_fields_address.append(_('city_address'))
    if not profile.exact_address:
        incomplete_fields_address.append(_('exact_address'))
    if not profile.postal_code:
        incomplete_fields_address.append(_('postal_code'))
    if not profile.order_notes:
        incomplete_fields_address.append(_('order_notes'))

    context = {
        'profile': profile,
        'username': username,
        'incomplete_fields_address': incomplete_fields_address,
    }

    return render(request, 'orders/profile_address.html', context)


def profile_address_edit_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    if request.method == 'POST':
        form = ProfileFormLocations(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('order:profile_address'))
    else:
        form = ProfileFormLocations(instance=profile)


    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'orders/profile_address_edit.html', context)


@login_required
def profile_comment_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    comments_user = Comment.objects.select_related('user').filter(user=current_user).prefetch_related('product').all()
    
    context = {
        'profile': profile,
        'username': username,
        'comments_user': comments_user,
    }

    return render(request, 'orders/profile_comment.html', context)


@login_required
def profile_comment_remove(request, comment_id):
    # 1. یافتن کامنت مورد نظر با ID و اطمینان از مالکیت کاربر
    try:
        comment_to_delete = get_object_or_404(Comment, id=comment_id, user=request.user)
    except Http404:
        messages.error(request, "شما اجازه حذف این کامنت را ندارید یا کامنت یافت نشد.")
        return redirect('order:profile_comment') # یا آدرس صفحه پروفایل خودتان

    # 2. حذف از دیتابیس
    comment_to_delete.delete()
    
    # 3. نمایش پیام موفقیت
    messages.success(request, "کامنت با موفقیت حذف شد.")
    
    # 4. ریدایرکت به صفحه پروفایل (برای اطمینان از نمایش لیست به‌روز شده)
    return redirect('order:profile_comment') # فرض می‌کنیم نام URL برای صفحه پروفایل شما 'profile_comment' است
