from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from datetime import date
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from decimal import Decimal, ROUND_HALF_UP

class Product(models.Model):
    PRODUCT_TYPE = [
        ('FL', _('Flower')),
        ('FER', _('Fertilizer')),
        ('TOOL', _('Gardening Tool')),
        ('SEED', _('Seed')),
        ('SOIL', _('Potting Soil')),
    ]
    INVENTORY_STATUS = [
        ('AVA', _('Available')),
        ('OFS', _('Out_of_stock')),
        ('PEN', _('Pending')),
        ('DIS', _('Discontinued')),
    ]

    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    sku = models.CharField(_('sku'), max_length=150, unique=True, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', verbose_name=_('category'))
    product_type = models.CharField(_('product_type'), max_length=4, choices=PRODUCT_TYPE)
    features = models.ForeignKey('Features', on_delete=models.CASCADE, related_name='product', verbose_name=_('features'))
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=True, null=True, related_name='products', verbose_name=_('brand'))
    inventory = models.ForeignKey('Inventory', on_delete=models.SET_NULL, null=True, related_name='product', verbose_name=_('inventory'))
    commodity_status = models.CharField(_('commodity_status'), max_length=3, choices=INVENTORY_STATUS, default='AVA')
    successful_sales_count = models.PositiveIntegerField(_('successful_sales_count'), default=0)
    base_price = models.DecimalField(_('base_price'), max_digits=10, decimal_places=2)
    short_description = models.CharField(_('short_description'), max_length=100)
    description = RichTextField(_('description'))
    tags = TaggableManager(_('tags'), blank=True)
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts', verbose_name=_('product_discounts'))
    discount_percentage = models.DecimalField(_('discount_percentage'), max_digits=5, decimal_places=2)
    start_date = models.DateField(_('start_date'), default=timezone.now)
    end_date = models.DateField(_('end_date'), default=timezone.now)
    is_active = models.BooleanField(_('is_active'), default=True)

    def __str__(self):
        return f'{self.product.name} - {self.discount_percentage}'

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_('subcategories'))

    def __str__(self):
        return self.name

class Inventory(models.Model):
    INVENTORY_STATUS = [
        ('AVA', _('Available')),
        ('NON', _('Non-available')),
        ('SPE', _('Special')),
    ]
    status = models.CharField(_('status'), max_length=3, choices=INVENTORY_STATUS, default='AVA')
    inventory = models.PositiveIntegerField(_('inventory'), default=0)

    def __str__(self):
        return f'{self.status}'

class Features(models.Model):
    PRODUCT_LIQUID_UNIT = [
        ('GR', _('Gram')),
        ('KG', _('KiloGram')),

        ('Ml', _('MilliLiter')),
        ('L', _('Liter')),
    ]
    PRODUCT_SOLIDS_UNIT = [
        ('Num', _('Number')),
        ('Pack', _('Packet')),
    ]
    PRODUCT_NUMBER_UNIT = [
        ('Cm', _('SantiMeter')),
        ('M', _('Meter')),
    ]
    name_features = models.CharField(_('name_features'), max_length=100)

    Length = models.DecimalField(_('Length'),decimal_places=2, max_digits=10, blank=True, null=True)
    Length_unit = models.CharField(_('Length_unit'),max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    Width = models.DecimalField(_('Width'),decimal_places=2, max_digits=10, blank=True, null=True)
    Width_unit = models.CharField(_('Width_unit'),max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    Height = models.DecimalField(_('Height'),decimal_places=2, max_digits=10, blank=True, null=True)
    Height_unit = models.CharField(_('Height_unit'),max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    pot_size = models.CharField(_('pot_size'), max_length=50, blank=True, null=True)

    number = models.DecimalField(_('number'), decimal_places=2, max_digits=10, blank=True, null=True)
    unit_counting = models.CharField(_('unit_counting'), max_length=4, choices=PRODUCT_SOLIDS_UNIT, blank=True, null=True)

    weight = models.DecimalField(_('weight'), decimal_places=2, max_digits=10, blank=True, null=True)
    weight_unit = models.CharField(_('weight_unit'), max_length=2, choices=PRODUCT_LIQUID_UNIT, blank=True, null=True)

    ingredients = models.CharField(_('ingredients'), max_length=250)
    care_tips = RichTextField(blank=True, null=True, verbose_name=_('care tipe'))
    usage_instructions = RichTextField(blank=True, null=True, verbose_name=_('usage instructions'))

    def __str__(self):
        return f'{self.name_features}'

class Order(models.Model):
    PAYMENT_STATUS = [
        ('PEN', _('Pending')),
        ('PAI', _('Paid')),
        ('CAN', _('Cancelled')),
        ('RET', _('Returned')),
    ]
    status = models.CharField(_('status'), max_length=3, choices=PAYMENT_STATUS, default='PEN')
    created_at = models.DateTimeField(_('created_at'), default=timezone.now)

    def __str__(self):
        return f'{self.status}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('items'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name=_('order_items'))
    quantity = models.DecimalField(_('quantity'), max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} * {self.product.name}'

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Brand_name'))
    description = RichTextField(blank=True, null=True, verbose_name=_('description'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = 'brands'
        ordering = ['name']

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('comments'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'))
    time_release_comment = models.DateTimeField(_('time_release_comment'), default=timezone.now)
    update_to = models.DateTimeField(_('update_to'), auto_now=True)
    body_comment = RichTextField(_('body_comment'), )
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('answer'))

    def __str__(self):
        return f'{self.product}'
