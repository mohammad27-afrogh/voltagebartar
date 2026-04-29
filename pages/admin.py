from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import NewsRoom, AboutUs

@admin.register(NewsRoom)
class NewsRoomAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'short_description',
        'category',
        'admin',
        'date_time_create',
        'is_published',
        'publish_date',
    ]

    prepopulated_fields = {
        'slug': ['title',]
    }
    search_fields = ['title', 'category', 'is_published']


@admin.register(AboutUs)
class AboutUsAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'title',
        'short_discription',
    ]