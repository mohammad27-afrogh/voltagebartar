from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse

from ckeditor.fields import RichTextField

class NewsRoom(models.Model):
    CATEGORIS_NEWSPOOM = [
        ('ANN', _('announcment')),
        ('CAM', _('campaign')),
        ('EVE', _('event')),
        ('MED', _('media')),
        ('UPD', _('update')),
        ('EDU', _('educational')),
    ]

    title = models.CharField(_('title news'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, blank=True, null=False, allow_unicode=True)
    short_description = models.TextField(_('short description news'), max_length=100)
    description = RichTextField(_('description news'))
    category = models.CharField(_('category'), max_length=3, choices=CATEGORIS_NEWSPOOM, default='ANN')
    image_newsroom = models.ImageField(_('cover_newsroom'), upload_to='pages/newsroom', blank=True, null=True)
    admin = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('admin'))
    date_time_create = models.DateTimeField(_('date time create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date time modified'), auto_now=True)
    is_published = models.BooleanField(_('published ?'), default=False)
    publish_date = models.DateTimeField(_('date time create'), null=True, blank=True)

    class Meta:
        verbose_name = _('news')
        verbose_name_plural = _('news')
        # اولویت نمایش بر اساس تاریخ انتشار است سپس تاریخ ایجاد
        ordering = ['-publish_date', '-date_time_create']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])