from django.db.models import Q

from rest_framework import viewsets, permissions
from .models import Province, City
from .serializers import CitySerializer, ProvinceSerializer

from dal import autocomplete


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

class ProvinceAutocomplete(autocomplete.Select2QuerySetView):
    """
    ویوی Autocomplete برای مدل Province .  جستجو بر اساس نام استان انجام میشود .

    """
    def get_queryset(self):
        qs = Province.objects.all()

        if self.q:
            # جستجو بر اساس نام استان 
            qs = qs.filter(name__icontains=self.q) 

        return qs

class CityAutocomplete(autocomplete.Select2QuerySetView):
    """
    ویوی Autocomplete برای مدل City . 
    جستجو هم بر اساس نام شهر و هم نام استان مربوطه انجام میشود .
    همچنین قابلیت فیلتر بر اساس استان انتخاب شده را دارد .
    
    """
    def get_queryset(self):
        # ابتدا تمام شهرها را در نظر میگیریم
        qs = City.objects.all()

        # فیلتر کردن شهرها بر اساس استانی که از قبل انتخاب شده است
        # این پارامتر province_id توسط ویجت ModelSelect2 و با استفاده از 'forward' ارسال میشود
        province_id = self.forwarded.get('province_address', None)

        if province_id:
            # اگر province_id دریافت شد . کوئری ست را به شهرهای آن استان محدود کن 
            qs = qs.filter(province=province_id)
            
        # اگر کاربر متنی را تایپ کرده باشد حاوی متن جستجو است (self.q)
        if self.q:
            # جستجو را هم بر روی نام شهر  و هم بر روی نام استان مربوط به آن شهر انجام میدهیم
            # Q objects  برای ترکیب شرط های  OR (یا) استفاده میشود 
            qs = qs.filter(name__icontains=self.q)
                # Q(name__icontains=self.q) | Q(province__name__icontains=self.q))

        return qs
