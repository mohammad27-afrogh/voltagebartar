from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin

from .models import Product, Discount, Category, Features, Brand, Comment, CategorySlider, Questions_and_answers, Answer

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
        'inventory',
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

    list_per_page = 10
    list_editable = ['inventory', 'base_price']

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
    autocomplete_fields = ['parent',]
    

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = [
        'name_features',
    ]
    search_fields = ['name_features',]


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

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
        list_display = [
            'admin',
            'question',
            'created_at',
        ]
