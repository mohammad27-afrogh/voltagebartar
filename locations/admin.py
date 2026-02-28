from django.contrib import admin

from .models import Province, City

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'province',
    )
    list_filter = ('province',)
    search_fields = ['name', ]
    autocomplete_fields = ['province', ]