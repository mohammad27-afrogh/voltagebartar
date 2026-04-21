from typing import Any

from _decimal import Decimal
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.cache import cache
from django.utils import timezone
from django.db.models import Q

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
    slug = models.SlugField(_('slug'), unique=True, blank=True, null=False)
    sku = models.CharField(_('sku'), max_length=150, unique=True, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('category'))
    product_type = models.CharField(_('product_type'), max_length=4, choices=PRODUCT_TYPE)
    cover_product = models.ImageField(_('cover_product'), upload_to='product/product_covers/', blank=True, null=True)
    features = models.ForeignKey('Features', on_delete=models.CASCADE, related_name='product',
                                 verbose_name=_('features'))
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=True, null=True, related_name='products',
                              verbose_name=_('brand'))
    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE, blank=True, null=True,
                                  related_name='inventory_link', verbose_name=_('inventory'))
    commodity_status = models.CharField(_('commodity_status'), max_length=3, choices=INVENTORY_STATUS, default='AVA')
    successful_sales_count = models.PositiveIntegerField(_('successful_sales_count'), default=0)
    base_price = models.DecimalField(_('base_price'), max_digits=10, decimal_places=2)
    short_description = models.CharField(_('short_description'), max_length=100)
    description = RichTextField(_('description'))
    tags = TaggableManager(_('tags'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)
    # ویژگی برای ذخیره تعداد بازدیدها
    view_count = models.IntegerField(
        default=0, # مقدار پیش‌فرض صفر
        verbose_name=_('Number of visits')
    )
    
    def __str__(self):
        return self.name

    # متد کمکی برای افزایش بازدید هنگام فراخوانی
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product_detail_by_slug', args=[self.slug])


    @property
    def final_price(self):
        if hasattr(self, 'best_discount_persentage') and self.best_discount_persentage:
            discount_factor = Decimal('1') - (self.best_discount_persentage / Decimal('100'))
            return (self.base_price * discount_factor).quantize(Decimal('0.01'))
        return self.base_price

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts',
                                verbose_name=_('product_discounts'))
    discount_percentage = models.DecimalField(_('discount_percentage'), max_digits=5, decimal_places=2)
    start_date = models.DateField(_('start_date'), default=timezone.now)
    end_date = models.DateField(_('end_date'), default=timezone.now)
    is_active = models.BooleanField(_('is_active'), default=True)

    def __str__(self):
        return f'{self.product.name} - % {self.discount_percentage} discount'

    def save(self, *args, **kwargs):
        # 1. اجرای عملیات ذخیره‌سازی اصلی
        super().save(*args, **kwargs)

        # 2. پاکسازی کش محصول مرتبط
        # این کار تضمین می‌کند که هرگاه تخفیفی تغییر کرد، قیمت مجدداً محاسبه شود.

        product_pk = self.product.pk

        # پاک کردن کش قیمت نهایی محصول (از متد final_price در مدل Product)
        cache.delete(f'product_final_price_{product_pk}')

        # پاک کردن کش‌های مربوط به نمایش لیست محصول و جزئیات محصول
        # (که احتمالاً در Viewها کش شده‌اند)
        cache.delete(f'product_detail_{product_pk}')
        cache.delete(f'product_list_data')  # اگر لیست کلی را کش کرده‌اید

class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=100, unique=True)
    slug = models.SlugField(_('Address (slug)'), unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name=_('Parent category')
    )
    caver_category = models.ImageField(_('cover_category'), upload_to='category/category_covers/', blank=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('Categories')
        ordering = ["name"]

    def __str__(self):
        # نمایش مسیر کامل دسته (مثلاً: گل و گیاه > سانسوریا)
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

    def get_all_descendants(self):
        """
        برمی‌گردونه تمام زیردسته‌های این دسته، در هر سطحی (بازگشتی)
        """
        descendants = set()

        def collect_children(cat):
            for sub in cat.subcategories.all():
                descendants.add(sub)
                collect_children(sub)

        collect_children(self)
        return list(descendants)

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'category_slug': self.slug})


class Inventory(models.Model):
    INVENTORY_STATUS = [
        ('AVA', _('Available')),
        ('NON', _('Non-available')),
        ('SPE', _('Special')),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_item',
                                verbose_name=_('product_name'))
    status = models.CharField(_('status'), max_length=3, choices=INVENTORY_STATUS, default='AVA')
    inventory = models.PositiveIntegerField(_('inventory'), default=0)

    def __str__(self):
        return f'{self.product}'


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

    Length = models.DecimalField(_('Length'), decimal_places=2, max_digits=10, blank=True, null=True)
    Length_unit = models.CharField(_('Length_unit'), max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    Width = models.DecimalField(_('Width'), decimal_places=2, max_digits=10, blank=True, null=True)
    Width_unit = models.CharField(_('Width_unit'), max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    Height = models.DecimalField(_('Height'), decimal_places=2, max_digits=10, blank=True, null=True)
    Height_unit = models.CharField(_('Height_unit'), max_length=20, choices=PRODUCT_NUMBER_UNIT, blank=True, null=True)

    pot_size = models.CharField(_('pot_size'), max_length=50, blank=True, null=True)

    number = models.DecimalField(_('number'), decimal_places=2, max_digits=10, blank=True, null=True)
    unit_counting = models.CharField(_('unit_counting'), max_length=4, choices=PRODUCT_SOLIDS_UNIT, blank=True,
                                     null=True)

    weight = models.DecimalField(_('weight'), decimal_places=2, max_digits=10, blank=True, null=True)
    weight_unit = models.CharField(_('weight_unit'), max_length=2, choices=PRODUCT_LIQUID_UNIT, blank=True, null=True)

    ingredients = models.CharField(_('ingredients'), max_length=250, blank=True, null=True)
    care_tips = RichTextField(blank=True, null=True, verbose_name=_('care tipe'))
    usage_instructions = RichTextField(blank=True, null=True, verbose_name=_('usage instructions'))

    def __str__(self):
        return f'{self.name_features}'


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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments_user', verbose_name=_('user'))
    time_release_comment = models.DateTimeField(_('time_release_comment'), default=timezone.now)
    update_to = models.DateTimeField(_('update_to'), auto_now=True)
    body_comment = RichTextField(_('body_comment'), )
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name=_('answer'))
    is_active = models.BooleanField(_('I recommend purchasing this product ?'), default=True)

    def __str__(self):
        return f'{self.product}'


class CategorySlider(models.Model):
    title = models.CharField(_('Ad Title'), max_length=100)
    subtitle = models.CharField(_('Short description'), max_length=200, blank=True)
    image = models.ImageField(_('caver slide'), upload_to='slider/category/')
    category = models.ForeignKey(
        'Category',
        verbose_name=_('Related category'),
        on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(_('Display order'), default=0)
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_category_url(self):
        """بازگرداندن لینک به صفحه دسته مربوطه"""
        return self.category.get_absolute_url()


class Questions_and_answers(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions',
                                verbose_name=_('Product questions and answers'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'))
    time_release_question = models.DateTimeField(_('time_release_question'), default=timezone.now)
    update_to = models.DateTimeField(_('update_to'), auto_now=True)
    body_question = RichTextField(_('body_question'), )
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                       verbose_name=_('answer'))
