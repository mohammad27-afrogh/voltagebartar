from .models import Category, Discount, Product
from datetime import timedelta
from django.utils import timezone

from django.db.models import Q


def context_processors(request):
    parent_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('name')
    return {'parent_categories': parent_categories}


def context_processors_discount(request):
    # این بخش مخصوص اسلایدر تخفیف‌های فعال است و درست کار می‌کند
    all_discounts = Discount.objects.filter(is_active=True).select_related('product')

    slider_discounts = list(all_discounts)[:5]

    return {
        'active_discounts_slider': slider_discounts,
        'active_discounts_count': len(all_discounts),
        'active_discounts_full': all_discounts,
    }


def context_successful_sales(request):
    successful_sales = (Product.objects.filter(successful_sales_count__gte=10)
                        .order_by('-successful_sales_count').prefetch_related('discounts'))

    # *** اصلاح: اضافه کردن ویژگی active_discount ***
    for product in successful_sales:
        # این خط، اولین تخفیف فعال را پیدا کرده و به عنوان active_discount اضافه می‌کند
        product.active_discount = product.discounts.filter(is_active=True).first()

    return {'successful_sales': successful_sales}


def context_latest_products(request):
    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=30)

    latest_products = (Product.objects.filter(Q(date_time_create__gte=one_month_ago) &
                                              Q(date_time_create__lte=default_time))
                       .prefetch_related('discounts')  # *** اصلاح: اضافه کردن prefetch_related ***
                       )

    # *** اصلاح: اضافه کردن ویژگی active_discount ***
    for product in latest_products:
        product.active_discount = product.discounts.filter(is_active=True).first()

    return {'latest_products': latest_products}
