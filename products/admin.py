from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Discount, Category, Inventory, Features, Order, OrderItem, Brand, Comment, CategorySlider, Questions_and_answers

class CommentsInline(admin.TabularInline):
    model = Comment
    fields = [
        'user',
        'body_comment',
    ]

@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'category',
        'successful_sales_count',
        'view_count',
        'base_price',
        'date_time_create',
    ]
    prepopulated_fields = {
        'slug': ['name',]
    }
    autocomplete_fields = ['category', 'features', 'brand', ]
    search_fields = ['name',]

    inlines = [
        CommentsInline,
    ]

@admin.register(Discount)
class DiscountAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'product',
        'discount_percentage',
        'start_date',
        'end_date',
        'is_active',
    ]
    autocomplete_fields = ['product',]
    search_fields = ['product',]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'parent',
    ]
    prepopulated_fields = {
        'slug': ['name',]
    }
    search_fields = ['name',]

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'status',
        'inventory',
    ]
    search_fields = ['product',]
    autocomplete_fields = ['product',]


@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = [
        'name_features',
        'pot_size',
        'unit_counting',
        'ingredients',
    ]
    search_fields = ['name_features',]

@admin.register(Order)
class OrderAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
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
    search_fields = ['order']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    search_fields = ['name',]

@admin.register(Comment)
class CommentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'product',
        'time_release_comment',
        'is_active',
    ]

@admin.register(CategorySlider)
class CategorySliderAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'title',
        'subtitle',
        'category',
        'is_active',
    ]

@admin.register(Questions_and_answers)
class QuestionsAndAnswersAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'user',
        'body_question',
    ]
