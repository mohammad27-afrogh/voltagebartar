from .models import Category, Discount, Product, Brand
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache

from django.db.models import Q, Prefetch


def context_processors(request):
    parent_categories = (Category.objects.filter(parent__isnull=True).prefetch_related('subcategories', 'subcategories__subcategories'))

    return {'parent_categories': parent_categories}


def context_processors_discount(request):
    time_now = timezone.now()
    cache_key = 'all_active_discount_data'

    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data
    
    else:

        slider_discount_qs = Discount.objects.filter(
            is_active = True,
            end_date__gt=time_now,
            start_date__lte=time_now,
        ).select_related('product').order_by('-start_date')
        slider_discounts_list = list(slider_discount_qs[:5])
        
        active_discounts_count = slider_discount_qs.count()

        result = {
            'active_discounts_slider': slider_discounts_list,
            'active_discounts_count': active_discounts_count
        }

        cache.set(cache_key, result, 3600)

        return result


def context_successful_sales(request):
    time_now = timezone.now()

    active_discounts_prefetch = Prefetch(
        'discounts',
        queryset = Discount.objects.filter(
            is_active = True,
            end_date__gt=time_now,
        ),
        to_attr = 'active_discount_list'
    )

    successful_sales = (Product.objects.filter(successful_sales_count__gte=10)
                        .order_by('-successful_sales_count').prefetch_related(active_discounts_prefetch))

    return {'successful_sales': successful_sales}


def context_latest_products(request):
    default_time = timezone.now()
    one_month_ago = default_time - timedelta(days=30)

    active_discounts_prefetch = Prefetch(
        'discounts',
        queryset = Discount.objects.filter(
            is_active = True,
            end_date__gte=default_time,
            start_date__lte=default_time,
        ).order_by('-start_date'),
        to_attr = 'active_discount_list'
    )

    latest_products = (Product.objects.filter(date_time_create__gte=one_month_ago).prefetch_related(active_discounts_prefetch))    

    return {'latest_products': latest_products}


def context_brand_products(request):
    brands = Brand.objects.all()

    return {'brands': brands}
