from django.db import models
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))