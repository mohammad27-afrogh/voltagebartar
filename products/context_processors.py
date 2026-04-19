from .models import Category, Discount, Product
from datetime import timedelta
from django.utils import timezone

from django.db.models import Q, Prefetch


def context_processors(request):
    parent_categories = (Category.objects.filter(parent__isnull=True).prefetch_related('subcategories', 'subcategories__subcategories'))

    return {'parent_categories': parent_categories}


def context_processors_discount(request):
    time_alan = timezone.now()

    # این بخش مخصوص اسلایدر تخفیف‌های فعال است و درست کار می‌کند
    all_discounts = Discount.objects.filter(is_active=True).filter(Q(end_date__gt=time_alan)).select_related('product')

    slider_discounts = list(all_discounts)[:5]

    return {
        'active_discounts_slider': slider_discounts,
        'active_discounts_count': len(all_discounts),
        'active_discounts_full': all_discounts,
    }


def context_successful_sales(request):
    time_now = timezone.now()

    active_discounts_prefetch = Prefetch(
        'discounts',
        queryset = Discount.objects.filter(
            is_active = True,
            end_date__gt=time_now,
        ).order_by('id'),
        to_attr = 'active_discount_list'
    )

    successful_sales = (Product.objects.filter(successful_sales_count__gte=10)
                        .order_by('-successful_sales_count').prefetch_related(active_discounts_prefetch))

    # *** اصلاح: اضافه کردن ویژگی active_discount ***
    for product in successful_sales:
        if product.active_discount_list:
            product.active_discount = product.active_discount_list[0]
        else:
            product.active_discount = None

    return {'successful_sales': successful_sales}


def context_latest_products(request):
    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=30)

    latest_products = (Product.objects.filter(Q(date_time_create__gte=one_month_ago) &
                                              Q(date_time_create__lte=default_time))
                       .prefetch_related('discounts')  # *** اصلاح: اضافه کردن prefetch_related ***
                       )

    # *** اصلاح: اضافه کردن ویژگی active_discount ***
    time_alan = timezone.now()
    for product in latest_products:
        product.active_discount = product.discounts.filter(is_active=True).filter(Q(end_date__gt=time_alan)).first()

    return {'latest_products': latest_products}
