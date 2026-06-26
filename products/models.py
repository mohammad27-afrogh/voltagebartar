from typing import Any

from _decimal import Decimal
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from django.db.models import Q
from django.db import models

from datetime import date
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from decimal import Decimal, ROUND_HALF_UP


class Product(models.Model):
    INVENTORY_STATUS = [
        ('AVA', _('Available')),
        ('OFS', _('Out_of_stock')),
        ('PEN', _('Pending')),
        ('DIS', _('Discontinued')),
    ]

    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True, null=False, allow_unicode=True)
    sku = models.CharField(_('sku'), max_length=150, unique=True, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products',
                                 verbose_name=_('category'))
    # cover_product = models.ImageField(_('cover_product'), upload_to='product/product_covers/', blank=True, null=True)
    features = models.ForeignKey('Features', on_delete=models.CASCADE, related_name='product',
                                 verbose_name=_('features'))
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=True, null=True, related_name='products',
                              verbose_name=_('brand'))
    inventory = models.PositiveIntegerField(_('inventory'), blank=True, null=False, default=0)
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

    class Meta:
        verbose_name_plural = _('product')
    
    def __str__(self):
        return self.name

    # متد کمکی برای افزایش بازدید هنگام فراخوانی
    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])


    @property
    def active_discount(self):
        if hasattr(self, 'active_discount_list'):
            return self.active_discount_list[0] if self.active_discount_list else None
        
        now = timezone.now().date()
        return Discount.objects.filter(
            product = self,
            is_active = True,
            start_date__lte = now,
            end_date__gte = now,
        ).order_by('-start_date').first()

    @property
    def final_price(self):
        discount = self.active_discount
        if discount:
            discount_factor = Decimal('1') - (discount.discount_percentage / Decimal('100'))
            return (self.base_price * discount_factor).quantize(Decimal('0.01'))
        return self.base_price


    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('products:product_detail_by_slug', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
                                verbose_name=_('product_covers'))
    cover_product = models.ImageField(_('cover_product'), upload_to='product/product_covers/', blank=True, null=True)

    def __str__(self):
        return f'Image for {self.product.name}'


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts',
                                verbose_name=_('product_discounts'))
    discount_percentage = models.DecimalField(_('discount_percentage'), max_digits=5, decimal_places=2)
    start_date = models.DateField(_('start_date'), default=timezone.now)
    end_date = models.DateField(_('end_date'), default=timezone.now)
    is_active = models.BooleanField(_('is_active'), default=True)

    class Meta:
        verbose_name_plural = _('Discount')

    def __str__(self):
        return f'{self.product.name} - % {self.discount_percentage} discount'

    def save(self, *args, **kwargs):
        # 1. اجرای عملیات ذخیره‌سازی اصلی
        super().save(*args, **kwargs)
        try:
            # 2. پاکسازی کش محصول مرتبط
            # این کار تضمین می‌کند که هرگاه تخفیفی تغییر کرد، قیمت مجدداً محاسبه شود.

            product_pk = self.product.pk

            # پاک کردن کش قیمت نهایی محصول (از متد final_price در مدل Product)
            cache.delete(f'product_final_price_{product_pk}')

            # پاک کردن کش‌های مربوط به نمایش لیست محصول و جزئیات محصول
            # (که احتمالاً در Viewها کش شده‌اند)
            cache.delete(f'product_detail_{product_pk}')
            cache.delete(f'product_list_data')  # اگر لیست کلی را کش کرده‌اید
            cache.delete('active_discount_slider_data')
            cache.delete('active_discount_count_data')
            cache.delete('all_active_discount_data')
        except ImportError:
            pass

class Category(models.Model):
    name = models.CharField(_('Category name'), max_length=100, unique=True)
    slug = models.SlugField(_('Address (slug)'), unique=True, allow_unicode=True)
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
        verbose_name_plural = _('Category')
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

class Features(models.Model):
    name_features = models.CharField(_('name_features'), max_length=100)
    short_discription = RichTextField(blank=True, null=True, verbose_name=_('short_discription'))
    discription = RichTextField(blank=True, null=True, verbose_name=_('discription'))
    image_Technical_specifications = models.ImageField(_('image Technical specifications'), upload_to='product/product_covers/', blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Features')

    def __str__(self):
        return f'{self.name_features}'


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Brand_name'))
    slug = models.SlugField(_('slug'), unique=True, blank=True, null=False, allow_unicode=True)
    cover_brand = models.ImageField(_('cover brand'), upload_to='brand/cover_brand/', blank=True, null=True)
    description = RichTextField(blank=True, null=True, verbose_name=_('description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'brand'
        verbose_name_plural = _('brands')
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

    class Meta:
        verbose_name_plural = _('Comment')

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
        verbose_name_plural = _('Category Slider')

    def __str__(self):
        return self.title

    def get_category_url(self):
        """بازگرداندن لینک به صفحه دسته مربوطه"""
        return self.category.get_absolute_url()


class Questions_and_answers(models.Model):
    CHOICES_QUESTION_AND_ANSWER = [
        ('LAR', _('Log in and register')),
        ('ORP', _('Order registration process')),
        ('OT', _('Order tracking')),
        ('RG', _('Returning goods')),
        ('DCG', _('Discount codes and gift cards')),
        ('OS', _('Other cases')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='questions',
                                verbose_name=_('Product questions and answers'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'))
    time_release_question = models.DateTimeField(_('time_release_question'), default=timezone.now)
    update_to = models.DateTimeField(_('update_to'), auto_now=True)
    body_question = RichTextField(_('body_question'), )
    answer_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_questions',
                                       verbose_name=_('answer'))
    category_question = models.CharField(_('category_question'), max_length=3, choices=[('', _('What part do you have a question about?'))] + CHOICES_QUESTION_AND_ANSWER)

    class Meta:
        verbose_name_plural = _('Questions and answers')

    def __str__(self):
        return self.body_question[:50]


class Answer(models.Model):
    question = models.ForeignKey(Questions_and_answers, on_delete=models.CASCADE, related_name='answers',
                                verbose_name=_('answer admin to question product'))
    admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('admin'))
    answer_text = models.TextField(_('body_question_answer'),)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name_plural = _('Answer')

    def __str__(self):
        return self.answer_text[:50]
