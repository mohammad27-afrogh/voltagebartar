import requests
import json
import uuid

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.db import transaction
from django.db.models import F
from django.conf import settings

from orders.models import Order, OrderItem

def payment_process_view(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://payment.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id} : {order.user.first_name} {order.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback')),
    }

    res = requests.post(
        url=zarinpal_request_url, 
        data=json.dumps(request_data), 
        headers=request_header
    )

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://payment.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error from zarinpal!')


def custom_success_page_view(request):
    return render(request, 'cart/cart_checkout_complete_buy.html')


def payment_callback_view(request):
    payment_authority = request.GET.get('authority')
    payment_status = request.GET.get('status')

    # اگر authority یا status نداریم، به صفحه خطا یا سبد خرید برگردان
    if not payment_authority or not payment_status:
        # می‌توانید به صفحه سبد خرید یا یک صفحه خطای عمومی ریدایرکت کنید
        return redirect(reverse('payment:custom_success')) # یا هر آدرس دیگری

    try:
        order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    except Order.DoesNotExist:
        # اگر سفارشی با این authority پیدا نشد، خطا را نمایش بده
        return render(request, 'cart/cart_checkout_complete_buy.html', context={
            'error_message': 'سفارش مربوطه یافت نشد.',
        })

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    # چک کردن status اولیه از request.GET
    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }
        request_data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': rial_total_price,
            'authority': payment_authority,
        }

        try:
            # استفاده از response بجای res برای وضوح بیشتر
            response = requests.post(
                url='https://payment.zarinpal.com/pg/v4/payment/verify.json',
                data=json.dumps(request_data),
                headers=request_header,
                timeout=10 # اضافه کردن timeout برای جلوگیری از بلاک شدن طولانی
            )
            response.raise_for_status() # این خط اگر status code پاسخ غیر 2xx بود، خطا ایجاد می‌کند

            response_json = response.json() # یک بار JSON را بخوانید

            errors_payload = response_json.get('errors')
            # بررسی وجود کلید 'errors' در پاسخ کلی زرین پال
            if errors_payload:
                error_code = errors_payload.get('code', 'N/A')
                error_message = errors_payload.get('message', 'خطای ناشناخته در پاسخ زرین پال')
                return render(request, 'cart/cart_checkout_complete_buy.html', context={
                    'order_obj': order,
                    'error_code': error_code,
                    'error_message': f"خطای زرین پال: {error_message}",
                })
            
            data_payload = response_json.get('data')
            # بررسی وجود کلید 'data'
            if data_payload:
                payment_code = data_payload.get('code')
                ref_id = data_payload.get('ref_id')

                if payment_code == 100:
                    # پرداخت موفق - آپدیت سفارش و ریدایرکت
                    order.is_paid = True
                    order.zarinpal_ref_id = ref_id
                    order.zarinpal_data = data_payload # ذخیره کامل پاسخ زرین پال
                    order.zarinpal_payment_code = payment_code
                    order.save()

                    order_item = order.items.select_related('product').all()
                    for item in order_item:
                        if item.product:
                            item.product.successful_sales_count = F('successful_sales_count') + item.quantity
                            item.product.save(update_fields=['successful_sales_count'])
                            item.product.inventory = F('inventory') - item.quantity
                            item.product.save(update_fields=['inventory'])
                
                    # ریدایرکت به صفحه تکمیل خرید
                    return redirect(reverse('payment:custom_success'))

                elif payment_code == 101:
                    # تراکنش قبلا تایید شده - فقط ریدایرکت
                    return redirect(reverse('payment:custom_success'))

                else:
                    # کدهای خطای دیگر زرین پال (مربوط به data)
                    # این بخش ممکن است کمتر پیش بیاید چون معمولا خطا در کلید errors می آید
                    return render(request, 'cart/cart_checkout_complete_buy.html', context={
                        'order_obj': order,
                        'error_code': payment_code,
                        'error_message': f"کد وضعیت نامعتبر از زرین پال: {payment_code}",
                    })
            else:
                 # پاسخ زرین پال نه خطا داشت و نه data
                return render(request, 'cart/cart_checkout_complete_buy.html', context={
                    'order_obj': order,
                    'error_message': 'پاسخ نامعتبر از زرین پال دریافت شد (فاقد data یا errors).',
                })

        except requests.exceptions.RequestException as e:
            # خطاهای مربوط به خود درخواست HTTP (مثل timeout, connection error)
            return render(request, 'cart/cart_checkout_complete_buy.html', context={
                'order_obj': order,
                'error_message': f"خطا در ارتباط با زرین پال: {e}",
            })
        except json.JSONDecodeError:
            # اگر پاسخ زرین پال JSON معتبر نباشد
            return render(request, 'cart/cart_checkout_complete_buy.html', context={
                'order_obj': order,
                'error_message': 'پاسخ دریافتی از زرین پال قابل پردازش نیست.',
            })

    else:
        # اگر payment_status در request.GET برابر 'OK' نبود
        # زرین پال ممکن است پارامترهای دیگری مثل status='NOK' و یا کدهای خطا را در URL بفرستد
        # بهتر است اینجا بر اساس status اولیه تصمیم بگیریم یا خطای کلی نشان دهیم
        # در حال حاضر، یک پیام خطای عمومی برمی‌گردانیم.
        # شما می‌توانید وضعیت واقعی را از request.GET.get('status') یا پارامترهای دیگر استخراج کنید.
        return render(request, 'cart/cart_checkout_complete_buy.html', context={
            'order_obj': order,
            'error_message': f"پرداخت ناموفق بود. وضعیت: {payment_status}",
        })
