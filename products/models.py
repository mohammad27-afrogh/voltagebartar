from django.db import models
from datetime import date
from django.utils import timezone

class Product(models.Model):
    PRODUCT_TYPE = [
        ('FL', 'Flower'),
        ('FER', 'Fertilizer'),
        ('TOOL', 'Gardening Tool'),
        ('SEED', 'Seed'),
        ('SOIL', 'Potting Soil'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    sku = models.CharField(max_length=150, unique=True, blank=True, null=True)
    category = models.Foreignkey('Category', on_delete=models.CASCADE, related_name='products')
    product_type = models.CharField(max_length=4, choices=PRODUCT_TYPE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

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
    slug = models.Slugfield(unique=True)
    parent_catigory = models.Foreignkey('self', on_delete=models.CASCADE, nul=True, blank=True, related_name='subcategories')
