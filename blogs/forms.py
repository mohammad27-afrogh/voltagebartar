from django import forms

from .models import Blog, Category, CommentBlog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'name',
            'slug',
            'category',
            'cover_blog',
            'short_description',
            'description',
            'tags',
            'date_time_create',
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'parent_category',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentBlog
        fields = [
            'body_comment',
            ]
