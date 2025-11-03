from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

class Blog(models.Model):
    name = models.CharField(_('name'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True, blank=True, null=False)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='blogs', verbose_name=_('category'))
    cover_blog = models.ImageField(_('cover_blog'), upload_to='blog/blog_covers/', blank=True)
    short_description = models.CharField(_('short_description'), max_length=100)
    description = RichTextField(_('description'))
    tags = TaggableManager(_('tags'))
    date_time_create = models.DateTimeField(_('date_time_create'), default=timezone.now)
    date_time_modified = models.DateTimeField(_('date_time_modified'), auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('blog_detail_by_slug', args=[self.slug])

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_('subcategories'))

    def __str__(self):
        return f'{self.name}'

class CommentBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments', verbose_name=_('comments'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_('user'))
    time_release_comment = models.DateTimeField(_('time_release_comment'), default=timezone.now)
    update_to = models.DateTimeField(_('update_to'), auto_now=True)
    body_comment = RichTextField(_('body_comment'), )
    answer_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('answer'))

    def __str__(self):
        return f'{self.blog}'