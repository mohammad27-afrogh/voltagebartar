from .models import Category

def context_processors(request):
    parent_categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('name')
    return {'parent_categories': parent_categories}

