from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import jdatetime
from .forms import AddressFormOrder, ProfileFormBasic, ProfileFormLocations
from cart.cart import Cart
from products.models import Comment, Product
from .models import OrderItem, Order, Profile, FavoriteProduct
from .serializers import FavoriteProductSerializer


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
                    OrderItem.objects.create(
                        order = order_obj,
                        product = product,
                        quantity = quantity,
                        price = product.base_price,
                    )

            cart.clear()

            if order_obj.pyment_price == 'HD':
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


@api_view(['GET', 'POST', 'DELET'])
@permission_classes([IsAuthenticated])
def toggle_favorite_api_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # دریافت 'GET' : نمایش لیست علاقه مندی های فعلی کاربر
    if request.method == 'GET':
        favorite = FavoriteProduct.objects.filter(user=request.user)
        serializer = FavoriteProductSerializer(favorite, many=True)
        return Response(serializer.data)


    #  افزودن 'POST' : اضافه کردن محصول به لیست 
    if request.method == 'POST':
        # بررسی کن آیا قبلا اضافه شده است یا نه 
        if FavoriteProduct.objects.filter(user=request.user, product=product).exists():
            return Response({'detail: این محصول از قبل در لیست شما وجود دارد.'}, status=status.HTTP_200_OK)

        # ایجاد آیتم جدید 
        serializer = FavoriteProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # حذف 'DELET': حذف محصول از لیست 
    if request.method == 'DELETE':
        favorite_item = get_object_or_404(FavoriteProduct, user=request.user, product=product)
        favorite_item.delete()
        return Response({'detail: محصول با موفقیت حذف شد.'}, status=status.HTTP_204_NO_CREATED)

    return Response(status=status.HTTP_405_NOT_ALLOWED)


class FavoriteListView(ListAPIView):
    # فقفط کاربیران لاگین شده میتونن این لیست رو ببینن
    permission_classes = [IsAuthenticated]
    # سریالایزری که برای نمایش هر آیتم استفاده می شود
    serializer_class = FavoriteProductSerializer

    def get_queryset(self):
        # request  رو فیلتر میکنیم تا فقط محصولات کاربر فعلی نمایش داده بشن 
        # request.user از طریق permission_classes  در دسترس است 
        return FavoriteProduct.objects.filter(user=self.request.user).select_related('product')


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


@login_required
def profile_comment_view(request):
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

    comments_user = Comment.objects.select_related('user').filter(user=current_user).prefetch_related('product').all()
    
    context = {
        'profile': profile,
        'username': username,
        'jalali_join_date_str': jalali_join_date_str,
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
