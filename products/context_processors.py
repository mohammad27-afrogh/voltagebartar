from .models import Category, Discount

def context_processors(request):
    parent_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('name')
    return {'parent_categories': parent_categories}

def context_processors_discount(request):
    all_discounts = Discount.objects.filter(is_active=True).select_related('product')

    slider_discounts = list(all_discounts)[:5]

    return {
        'active_discounts_slider': slider_discounts,
        'active_discounts_count': len(all_discounts),
        'active_discounts_full': all_discounts,
    }