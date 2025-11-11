from rest_framework.routers import DefaultRouter
from locations.views import CityViewset, ProvinceViewsets

router = DefaultRouter()
router.register(r'province', ProvinceViewsets)
router.register(r'cities', CityViewset)

urlpatterns = router.urls