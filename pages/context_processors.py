from products.models import CategorySlider


def context_slider_category_home(request):
    sliders = CategorySlider.objects.filter(is_active=True).order_by('order')

    return {'sliders': sliders}
