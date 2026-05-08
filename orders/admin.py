from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Order, OrderItem, Profile

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'product', 'quantity', 'price', ]

@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'display_order_id',
        'first_name',
        'phone_number',
        'national_number',
        'postal_code',
        'date_time_create',
        'is_paid',
        'status',
        'payment_price',
    ]

    def display_order_id(self, obj):
        return str(obj.id)
    display_order_id.shoit_discription = 'Order ID'

    autocomplete_fields = ['province_address', 'city_address', ]

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
        'date_time_create',
    ]

@admin.register(Profile)
class ProfileAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'phone_number',
        'national_number',
        'province_address',
        'city_address',
        'exact_address',
        'postal_code',
        'email',
        'order_notes',
        'date_time_create',
        'date_time_modified',
        'Receive_the_newsletter'
    ]
    autocomplete_fields = ['province_address', 'city_address']

