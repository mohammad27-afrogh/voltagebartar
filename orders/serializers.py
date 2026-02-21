from rest_framework import serializers
from .models import FavoriteProduct
from products.models import Product, Comment

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'base_price', 'cover_product']  # هر فیلدی که می‌خوای نمایش بدی

class SuggestProductComment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['is_active']

class FavoriteProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    Suggest_product = SuggestProductComment(read_only=True)
    class Meta:
        model = FavoriteProduct
        fields = ['product', 'date_added']
