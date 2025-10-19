from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import date
from taggit.managers import TaggableManager

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
    inventory = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    commodity_status = models.CharField(max_length=3, choices=INVENTORY_STATUS, default='AVA')
    successful_sales_count = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager(blank=True)

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
        best_discount = self.active_discounts.order_by('_discount_percentage').first()

        if best_discount:
            discount_factor = 1 - (best_discount.discount_percentage / 100)
            discounted_price = self.base_price * discount_factor
            return discounted_price.quantize(models.DecimalField().quantize(0))
        else:
            return self.base_price

class Discount(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='discounts')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=True)
    is_active = models.BooleanField(default=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, nul=True, blank=True, related_name='subcategories')

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
    Length = models.BooleanField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    Width = models.BooleanField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    Height = models.BooleanField(max_length=3, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)
    pot_size = models.BooleanField(max_length=5, blank=True, null=True)

    unit = models.CharField(max_length=4, choices=PRODUCT_SOLIDS_UNIT, blank=True, null=True)
    weight = models.CharField(max_length=2, choices=PRODUCT_LIQUID_UNIT, blank=True, null=True)

    ingredients = models.CharField(max_length=250)
    care_tips = models.TextField(blank=True, null=True)
    usage_instructions = models.TextField(blank=True, null=True)

class Order(models.Model):
    PAYMENT_STATUS = [
        ('PEN', 'Pending'),
        ('PAI', 'Paid'),
        ('CAN', 'Cancelled'),
        ('RET', 'Returned'),
    ]
    status = models.CharField(max_length=3, choices=PAYMENT_STATUS, default='PEN')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    @receiver(post_save, sender=Order)
    def update_successful_sales(sender, instance, **kwargs):
        if instance.status == 'PAID':
            for item in instance.items.all():
                product = item.product
                product.successful_sales_count += int(item.quantity)
                product.inventory -= item.quantity
                product.save()

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Brand name')
    description = models.TextField(blank=True, null=True, verbose_name='description')

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['name']