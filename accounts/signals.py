from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import settings
# تابع مهمی که برای خواندن قالب‌ها لازم داریم:
from django.template.loader import render_to_string
# برای گرفتن اطلاعات سایت
from django.contrib.sites.models import Site
# برای گرفتن سال جاری
import datetime


# مدل User را دریافت می‌کنیم
User = get_user_model()

# دکوراتور receiver سیگنال post_save را به این تابع متصل می‌کند
# sender=User یعنی این تابع زمانی اجرا شود که تغییری در مدل User رخ می‌دهد
@receiver(post_save, sender=User)
def send_welcome_email_on_signup(sender, instance, created, **kwargs):
    # 'created' اگر یک کاربر جدید در حال ایجاد شدن باشد True است
    if created:
        # --- آماده‌سازی اطلاعات برای قالب ایمیل ---
        # اطلاعات سایت فعلی را از دیتابیس می‌گیریم
        current_site = Site.objects.get_current()

        # اطلاعاتی که قرار است به قالب HTML پاس داده شود
        context = {
            'username': instance.username, # نام کاربری کاربر جدید
            'site_name': current_site.name, # نام سایت از تنظیمات Django Sites
            'site_url': f"http://{current_site.domain}", # آدرس سایت
            'current_year': datetime.date.today().year, # سال جاری
        }

        # --- خواندن قالب ایمیل HTML ---
        # render_to_string قالب مشخص شده را پیدا کرده و با context پر می‌کند
        html_content = render_to_string('account/welcome_email.html', context)

        # --- تنظیمات ایمیل ---
        subject = f'به {current_site.name} خوش آمدید!' # عنوان ایمیل
        sender_email = settings.EMAIL_HOST_USER # ایمیل فرستنده از تنظیمات settings.py
        recipient_email = instance.email # ایمیل کاربر جدید

        # --- ارسال ایمیل ---
        try:
            email = EmailMessage(
                subject,          # عنوان
                html_content,     # محتوای HTML
                sender_email,     # فرستنده
                [recipient_email], # گیرنده(ها)
            )
            # مشخص می‌کنیم که محتوا از نوع HTML است
            email.content_subtype = "html"
            # ارسال ایمیل
            email.send()
            print(f"ایمیل خوش‌آمدگویی (با قالب HTML) برای {instance.username} با موفقیت ارسال شد.")
        except Exception as e:
            # در صورت بروز خطا، پیام خطا را چاپ می‌کنیم
            print(f"خطا در ارسال ایمیل خوش‌آمدگویی (قالب HTML) برای {instance.username}: {e}")
