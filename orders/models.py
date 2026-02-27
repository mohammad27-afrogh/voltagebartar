from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone

from products.models import Product
from locations.models import Province, City
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

class Order(models.Model):
    pyment_price = [
        ('PP', _('Pyment Price')),
        ('HD', _('House Door')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    is_paid = models.BooleanField(_('is paid'), default=False)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    phone_number = PhoneNumberField(_('phone number'))
    national_number = models.CharField(_('national number'), max_length=10)
    province_address = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('province'))
    city_address = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('city'))
    exact_address = models.CharField(_('exact address'), max_length=700)
    postal_code = models.IntegerField(_('postal code'), null=True, max_length=10)
    email = models.EmailField(_('email'))
    order_notes = RichTextField(_('order notes'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)
    zarinpal_authority = models.CharField(max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(max_length=255, blank=True)
    zarinpal_data = models.TextField(blank=True)
    pyment_price = models.CharField(_('other pyment price'), max_length=2, choices=pyment_price)


    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.quantity * item.price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_items', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.PositiveIntegerField(_('price'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)

    def __str__(self):
        return f'OrderItem {self.id}: {self.product} * {self.quantity} (price:{self.price})'

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    phone_number = PhoneNumberField(_('phone number'))
    national_number = models.CharField(_('national number'), max_length=10)
    province_address = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, verbose_name=_('province'))
    city_address = models.ForeignKey(City, on_delete=models.CASCADE, null=True, verbose_name=_('city'))
    exact_address = models.CharField(_('exact address'), max_length=700)
    postal_code = models.IntegerField(_('postal code'), null=True, max_length=10)
    email = models.EmailField(_('email'))
    order_notes = RichTextField(_('order notes'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)
    Receive_the_newsletter = models.BooleanField(_('Receive the newsletter'), default=True)


    def __str__(self):
        return f"Profile of {self.user.username}"

class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        # اطمینان از اینکه یک کاربر فقط یک بار می‌تواند یک محصول را به علاقه‌مندی اضافه کند
        unique_together = ('user', 'product')
        verbose_name = "محصول مورد علاقه"
        verbose_name_plural = "محصولات مورد علاقه"

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"