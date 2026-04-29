from django import forms
from .models import NewsRoom, AboutUs


class NewsRoomForms(forms.ModelForm):
    class Meta:
        model = NewsRoom
        fields = [
            'title',
            'slug',
            'short_description',
            'description',
            'category',
            'image_newsroom',
            'admin',
            'date_time_create',
            'date_time_modified',
            'is_published',
            'publish_date',
        ]

class AboutUsForms(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields = [
            'title',
            'short_discription',
            'discription',
        ]