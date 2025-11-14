from rest_framework.routers import DefaultRouter
from locations.views import CityViewSet, ProvinceViewSets

router = DefaultRouter()
router.register(r'province', ProvinceViewSets)
router.register(r'cities', CityViewSet)

urlpatterns = router.urls