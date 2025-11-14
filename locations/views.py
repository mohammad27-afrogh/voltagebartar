from rest_framework import viewsets, permissions
from .models import Province, City
from .serializers import CitySerializer, ProvinceSerializer


class ProvinceViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        province_id = self.request.query_params.get('province_id')
        queryset = self.queryset

        if province_id:
            queryset = queryset.filter(province_id=province_id)
        return queryset
