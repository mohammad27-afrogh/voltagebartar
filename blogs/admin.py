from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Blog, Category

@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'category',
        'short_description',
        'date_time_create',
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]