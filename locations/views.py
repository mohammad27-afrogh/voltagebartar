from rest_framework import viewsets, permissions
from .models import Province, City
from .serializers import CitySerializer, ProvinceSerializer


class ProvinceViewsets(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permissions_class = [permissions.IsAuthenticatedOrReadOnly]

class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permissions_class = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        province_id = self.request.query_parms.get('province_id')

        if province_id:
            return queryset.filter(province_id=province_id)
        return queryset
