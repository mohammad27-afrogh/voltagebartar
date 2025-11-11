from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]

@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'first_name',
        'phone_number',
        'national_number',
        'province_address',
        'city_address',
        'exact_address',
        'date_time_create',
        'is_paid',
    ]

    inlines = [
        OrderItemInline,
    ]

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'quantity',
        'price',
    ]
