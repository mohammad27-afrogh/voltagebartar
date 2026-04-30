from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from products.models import Product

from django.conf import settings

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
        verbose_name = _('Favorite Product')
        verbose_name_plural = _('Favorite Product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
