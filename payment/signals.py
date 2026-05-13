from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext as _

from orders.models import Order
from utils.sms import send_sms_kavenegar

@receiver(post_save, sender=Order)
def order_post_save_handler(sender, instance, created, **kwargs):
    #هنوز ارسال نشده sms_send=False پیامک وقتی ارسال شود که 
    # سفارش به وضعیت مجازه (پرداخت شده یا انتظار)رسیده باشد
    if instance.sms_send:
        return
    
    allowed_statuses = {'PAI', 'PEN'}

    if instance.status not in allowed_statuses:
        return

    customer_message = _("Bartar Voltage store \n\n" \
    "Your order with code {} Successfully registered.\n" \
    "Preparing to send.").format(instance.id)

    admin_message = _("Bartar Voltage store \n\n" \
    "A new order with code {} has been placed.\n" \
    "Please check for delivery.").format(instance.id)

    # ارسال پیامک
    send_sms_kavenegar(instance.phone_number, customer_message)
    send_sms_kavenegar(settings.ADMIN_PHONE_NUMBER, admin_message)

    # علامت گذاری کد پیامک ارسال شده
    instance.sms_send = True
    instance.save(update_fields=['sms_send'])
