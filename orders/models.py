from django.db import models
from django.db import transaction
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone

from uuid import uuid4

from products.models import Product
from locations.models import Province, City
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

class Order(models.Model):
    PYMENT_PRICE_CHOICESS = [
        ('PP', _('Pyment Price')),
        ('HD', _('House Door')),
    ]
    PAYMENT_STATUS = [
        ('PEN', _('Pending')),
        ('PAI', _('Paid')),
        ('CAN', _('Cancelled')),
        ('RET', _('Returned')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    is_paid = models.BooleanField(_('is paid'), default=False)
    status = models.CharField(_('status'), max_length=3, choices=PAYMENT_STATUS, default='PEN')

    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=200)
    phone_number = PhoneNumberField(_('phone number'))
    national_number = models.CharField(_('national number'), max_length=10)

    province_address = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_('province'))
    city_address = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('city'))
    exact_address = models.CharField(_('exact address'), max_length=700)
    postal_code = models.CharField(_('postal code'), max_length=10, null=True)
    email = models.EmailField(_('email'))
    order_notes = RichTextField(_('order notes'))

    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)

    zarinpal_authority = models.CharField(_('zarinpal authority'), max_length=255, blank=True)
    zarinpal_ref_id = models.CharField(_('zarinpal ref id'), max_length=255, blank=True)
    zarinpal_data = models.TextField(_('zarinpal data'), blank=True)
    zarinpal_payment_code = models.CharField(_('zarinpal payment code'), max_length=100, blank=True)
    payment_price = models.CharField(_('other pyment price'), max_length=2, choices=PYMENT_PRICE_CHOICESS)
    sms_send = models.BooleanField(_('sms send'), default=False)


    class Meta:
        verbose_name_plural = _('Order')

    def __str__(self):
        return f'Order {self.id} for {self.user}'

    @transaction.atomic
    def get_total_price(self):
        total_price = sum(item.quantity * item.price for item in self.items.all())

        shipping_cost = 0 if self.city_address.name == 'تهران' else 500000
        return total_price + shipping_cost

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_items', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.PositiveIntegerField(_('price'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)

    class Meta:
        verbose_name_plural = _('Order Item')

    def __str__(self):
        return f'OrderItem {self.id}: {self.product.name} * {self.quantity} (price:{self.price})'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.price = self.product.final_price
        super().save(*args, **kwargs)


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

    class Meta:
        verbose_name_plural = _('Profile')

    def __str__(self):
        return f"Profile of {self.user.username}"
