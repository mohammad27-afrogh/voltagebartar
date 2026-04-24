from django import forms
from .models import (Product,
                     Discount,
                     Category,
                     Inventory,
                     Features,
                     Brand,
                     Comment,
                     CategorySlider,
                     Questions_and_answers,
                     Answer,
                     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'sku',
            'view_count',
            'category',
            'product_type',
            'successful_sales_count',
            'commodity_status',
            'base_price',
            'short_description',
            'date_time_create',
        ]

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = [
            'product',
            'discount_percentage',
            'start_date',
            'end_date',
            'is_active',
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
            'parent',
        ]

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            'product',
            'status',
            'inventory',
        ]

class FeaturesForm(forms.ModelForm):
    class Meta:
        model = Features
        fields = [
            'name_features',
            'Length_unit',
            'Length',
            'Width_unit',
            'Width',
            'Height_unit',
            'Height',
            'pot_size',
            'number',
            'unit_counting',
            'weight',
            'weight_unit',
            'ingredients',
            'care_tips',
            'usage_instructions',
        ]

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = [
            'name',
            'description',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body_comment',
            'is_active',
        ]

class CategorySliderForm(forms.ModelForm):
    class Meta:
        model = CategorySlider
        fields = [
            'title',
            'subtitle',
            'image',
        ]

class QuestionsAndAnswersForm(forms.ModelForm):
    class Meta:
        model = Questions_and_answers
        fields = [
            'body_question',
            'category_question',
        ]

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            'admin',
            'answer_text',
            'created_at',
        ]
        