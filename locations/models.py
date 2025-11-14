from django.db import models
from django.utils.translation import gettext_lazy as _


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('name_province'))

    class Meta:
        verbose_name = 'province'
        verbose_name_plural = 'provinces'

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name = 'cities', verbose_name =_('province'))
    name = models.CharField(max_length=100, verbose_name =_('city_name'))

    class Meta:
        verbose_name = 'county'
        verbose_name_plural = 'cities'
        unique_together = ('province', 'name')

    def __str__(self):
        return f'{self.name} ({self.province.name})'
