from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse

import jdatetime
from .forms import OrderForm, ProfileFormBasic, ProfileFormLocations
from cart.cart import Cart
from .models import OrderItem, Order, Profile

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
    
    profile, created  = Profile.objects.get_or_create(user=current_user)

    username = current_user

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")


    # گرفتن تاریخ آپدیت ویرایش پروفایل کاربر
    gregorian_profile_date = profile.date_time_modified
    jalali_profile_date_str = "تاریخ نامشخص"
    if gregorian_profile_date:
        jalali_profile_date = jdatetime.datetime.fromgregorian(datetime=gregorian_profile_date)
        # فرمت دلخواه: سال/ماه/روز ساعت:دقیقه
        jalali_profile_date_str = jalali_profile_date.strftime("%Y/%m/%d %H:%M")

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
        'jalali_join_date_str': jalali_join_date_str,
        'jalali_profile_date_str': jalali_profile_date_str
    }
    
    return render(request, 'orders/profile_user.html', context)


def profile_user_create_view(request):

    return render(request, 'orders/profile_create.html')



@login_required
def profile_user_edit_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")


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
        'jalali_join_date_str': jalali_join_date_str,
    }

    return render(request, 'orders/profile_user_edit.html', context)



@login_required
def profile_orders_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    order = get_object_or_404(
        Order.objects.select_related('city_address', 'province_address'),
        user=current_user
    )

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")
    
    orders_whit_items = Order.objects.prefetch_related('items').all()

    if order.city_address == 'Tehra':
        total_price_city = order.get_total_price()
    else:
        total_price_city = order.get_total_price() + 500000

    context = {
        'username': username,
        'profile': profile,
        'jalali_join_date_str': jalali_join_date_str,
        'orders_whit_items': orders_whit_items,
        'total_price_city': total_price_city,
    }

    return render(request, 'orders/profile_order.html', context)


@login_required
def profile_order_view(request):
    current_user = request.user
    username = current_user
    # 1. پیدا کردن شیء ORDER تکی با استفاده از get_object_or_404
    # این شیء تکی (object) دارای فیلدهای آدرس است.
    # ما از select_related برای بهینه‌سازی دسترسی به آدرس‌ها استفاده می‌کنیم.

    order = get_object_or_404(
        Order.objects.select_related('city_address', 'province_address'),
        user=current_user
    )

    profile, created  = Profile.objects.get_or_create(user=current_user)

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")

    order_items_product = order.items.select_related('product').all()


    if order.city_address == 'Tehra':
        total_price_city = order.get_total_price()
    else:
        total_price_city = order.get_total_price() + 500000



    context = {
        'username': username,
        'profile': profile,
        'jalali_join_date_str': jalali_join_date_str,
        'order': order,
        'order_items_product': order_items_product,
        'total_price_city': total_price_city,
    }

    
    return render(request, 'orders/profile_order_view.html', context)




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
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    incomplete_fields_address = []
    if not profile.phone_number:
        incomplete_fields.append(_('phone_number'))
    if not profile.province_address:
        incomplete_fields.append(_('province_address'))
    if not profile.city_address:
        incomplete_fields.append(_('city_address'))
    if not profile.exact_address:
        incomplete_fields.append(_('exact_address'))
    if not profile.postal_code:
        incomplete_fields.append(_('postal_code'))
    if not profile.order_notes:
        incomplete_fields.append(_('order_notes'))

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")

    context = {
        'profile': profile,
        'username': username,
        'incomplete_fields_address': incomplete_fields_address,
        'jalali_join_date_str': jalali_join_date_str,
    }

    return render(request, 'orders/profile_address.html', context)


def profile_address_edit_view(request):
    # 1. دسترسی به شیء کاربر احراز هویت شده
    current_user = request.user
    username = current_user
    profile, created  = Profile.objects.get_or_create(user=current_user)

    # گرفتن تاریخ ثبت نام کاربر
    gregorian_join_date = current_user.date_joined  
    jalali_join_date_str = "تاریخ نامشخص"

    if gregorian_join_date:
        jalali_join_date = jdatetime.datetime.fromgregorian(datetime=gregorian_join_date)
        # فرمت تاریخ: سال/ماه/روز ساعت:دقیقه
        jalali_join_date_str = jalali_join_date.strftime("%Y/%m/%d %H:%M:%S")

    if request.method == 'POST':
        form = ProfileFormLocations(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('order:profile_address'))
    else:
        form = ProfileFormLocations(instance=profile)


    context = {
        'profile': profile,
        'jalali_join_date_str': jalali_join_date_str,
        'form': form,
    }

    return render(request, 'orders/profile_address_edit.html', context)

# @login_required
# def remove_from_profile_address(request, current_user):
#     address = OrderItem(request)

#     product = get_object_or_404(Order, slug=current_user)
#     address.remove(product)

#     return redirect('order:remove_profile_address')

@login_required
def profile_comment_view(request):

    return render(request, 'orders/profile_comment.html')

