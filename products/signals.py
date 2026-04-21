from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from orders.models import Order

@receiver(post_save, sender=Order)
def update_successful_sales(sender, instance, **kwargs):
    if instance.status == 'PAI':
        for item in instance.items.all():
            product = item.product
            product.successful_sales_count += int(item.quantity)
            product.inventory -= item.quantity
            product.save()