from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import FavoriteProduct

@admin.register(FavoriteProduct)
class FavoriteProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'date_added',
    ]
