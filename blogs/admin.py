from django.contrib import admin

from jalali_date.admin import ModelAdminJalaliMixin

from .models import Blog, Category, CommentBlog

class CommentsInline(admin.TabularInline):
    model = CommentBlog
    fields = [
        'user',
        'body_comment',
    ]

@admin.register(Blog)
class BlogAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'user',
        'name',
        'slug',
        'category',
        'short_description',
        'date_time_create',
    ]
    autocomplete_fields = ['category',]
    search_fields = ['name',]

    prepopulated_fields = {
        'slug': ['name',]
    }

    inlines = [
        CommentsInline,
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
    ]

    prepopulated_fields = {
        'slug': ['name',]
    }
    search_fields = ['name',]

@admin.register(CommentBlog)
class CommentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = [
        'blog',
        'time_release_comment',
    ]
