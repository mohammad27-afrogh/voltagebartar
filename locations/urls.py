from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CityViewSet, ProvinceViewSets, ProvinceAutocomplete, CityAutocomplete

router = DefaultRouter()
router.register(r'province', ProvinceViewSets)
router.register(r'cities', CityViewSet)

app_name = 'locations'

urlpatterns = [
    path('', include(router.urls)),
    path('province_autocomplete/', ProvinceAutocomplete.as_view(), name='province_autocomplete'),
    path('city_autocomplete/', CityAutocomplete.as_view(), name='city_autocomplete'),
]
