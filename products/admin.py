from django.contrib import admin

from .models import Product, Discount, Category, Inventory, Features, Order, OrderItem, Brand, Comment

class CommentsInline(admin.TabularInline):
    model = Comment
    fields = [
        'user',
        'body_comment',
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'successful_sales_count',
        'base_price',
        'date_time_create',
    ]

    inlines = [
        CommentsInline,
    ]

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'discount_percentage',
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'status',
        'inventory',
    ]

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = [
        'Length',
        'Width',
        'Height',
        'pot_size',
        'unit',
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'status',
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'quantity',
    ]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'time_release_comment',
    ]
