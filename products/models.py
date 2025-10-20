from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from datetime import date
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from decimal import Decimal, ROUND_HALF_UP

class Product(models.Model):
    PRODUCT_TYPE = [
        ('FL', 'Flower'),
        ('FER', 'Fertilizer'),
        ('TOOL', 'Gardening Tool'),
        ('SEED', 'Seed'),
        ('SOIL', 'Potting Soil'),
    ]
    INVENTORY_STATUS = [
        ('AVA', 'Available'),
        ('OFS', 'Out_of_stock'),
        ('PEN', 'Pending'),
        ('DIS', 'Discontinued'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=150, unique=True, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=4, choices=PRODUCT_TYPE)
    features = models.ForeignKey('Features', on_delete=models.CASCADE, related_name='product')
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=True, null=True, related_name='products', verbose_name='brand')
    inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True, related_name='product')
    commodity_status = models.CharField(max_length=3, choices=INVENTORY_STATUS, default='AVA')
    successful_sales_count = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=100)
    description = RichTextField()
    tags = TaggableManager(blank=True)
    date_time_create = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def is_on_sale(self):
        today = timezone.now().date()
        return self.discounts.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        ).exists()

    @property
    def active_discounts(self):
        today = timezone.now().date()
        return self.discounts.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today,
        )

    @property
    def final_price(self):
        best_discount = self.active_discounts.order_by('discount_percentage').first()

        if best_discount:
            discount_factor = 1 - (best_discount.discount_percentage / 100)
            discounted_price = self.base_price * discount_factor
            return discounted_price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            return f'{self.base_price}'

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product.name} - {self.discount_percentage}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Inventory(models.Model):
    INVENTORY_STATUS = [
        ('AVA', 'Available'),
        ('NON', 'Non-available'),
        ('SPE', 'Special'),
    ]
    status = models.CharField(max_length=3, choices=INVENTORY_STATUS, default='AVA')
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.status

class Features(models.Model):
    PRODUCT_LIQUID_UNIT = [
        ('GR', 'Gram'),
        ('KG', 'KiloGram'),

        ('Ml', 'MilliLiter'),
        ('L', 'Liter'),
    ]
    PRODUCT_SOLIDS_UNIT = [
        ('Num', 'Number'),
        ('Pack', 'Packet'),
    ]
    PRODUCT_NUMBER_UNIT = [
        ('Cm', 'SantiMeter'),
        ('M', 'Meter'),
    ]
    Length = models.DecimalField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    Width = models.DecimalField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    Height = models.DecimalField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    pot_size = models.CharField(max_length=5, blank=True, null=True)

    unit = models.CharField(max_length=4, choices=PRODUCT_SOLIDS_UNIT, blank=True, null=True)
    weight = models.CharField(max_length=2, choices=PRODUCT_LIQUID_UNIT, blank=True, null=True)

    ingredients = models.CharField(max_length=250)
    care_tips = RichTextField(blank=True, null=True, verbose_name='care tipe')
    usage_instructions = RichTextField(blank=True, null=True, verbose_name='usage instructions')

    def __str__(self):
        return f'Features for product unit: {self.unit or '-'}'

class Order(models.Model):
    PAYMENT_STATUS = [
        ('PEN', 'Pending'),
        ('PAI', 'Paid'),
        ('CAN', 'Cancelled'),
        ('RET', 'Returned'),
    ]
    status = models.CharField(max_length=3, choices=PAYMENT_STATUS, default='PEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} * {self.product.name}'

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Brand name')
    description = RichTextField(blank=True, null=True, verbose_name='description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['name']

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    time_release_comment = models.DateTimeField(auto_now_add=True)
    update_to = models.DateTimeField(auto_now=True)
    body_comment = RichTextField()
    answer_comment = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.product
