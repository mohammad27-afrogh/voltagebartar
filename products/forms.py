from django import forms
from .models import Product, Discount, Category, Inventory, Features, Order, OrderItem, Brand, Comment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'sku',
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
            'parent_category',
        ]

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            'status',
            'inventory',
        ]

class FeaturesForm(forms.ModelForm):
    class Meta:
        model = Features
        fields = [
            'Length',
            'Width',
            'Height',
            'pot_size',
            'unit',
            'weight',
            'ingredients',
            'care_tips',
            'usage_instructions',
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status',
            'created_at',
        ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            'order',
            'product',
            'quantity',
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
        model = comment
        fields = [
            'product',
            'user',
            'time_release_comment',
            'body_comment',
            'answer_comment',
            ]
