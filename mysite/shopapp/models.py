from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.db.models import CASCADE


def product_preview_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/preview/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )


class Product(models.Model):
    """
    Модель Product представляет товар,
    который можно продавать в интернет-магазине

    Заказы тут :model: `shopapp.Order`
    """
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']

    name = models.CharField(max_length=100, verbose_name=_('наименование'), db_index=True)
    description = models.TextField(null=False, blank=True, verbose_name = _('описание'), db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name = _('цена'))
    discount = models.SmallIntegerField(default=0, verbose_name = _('скидка'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = _('создано'))
    archived = models.BooleanField(default=False, verbose_name = _('архивирован'))
    created_by = models.ForeignKey(User, on_delete=CASCADE, related_name="products", verbose_name = _('создано'), null=True, blank=True)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path, verbose_name = _('превью'))

    # @property
    # def description_short(self) ->str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48]+'...'

    def __str__(self) -> str:
        return f'Product(pk={self.pk}, name={self.name!r})'


def product_images_directory_path(instance: 'Product', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True, verbose_name = _('адрес доставки'))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name = _('промокод'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name = _('создано'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name = _('пользователь'))
    products = models.ManyToManyField(Product, related_name='orders', verbose_name = _('товары'))
    receipt = models.FileField(null=True, upload_to='orders/receipts', verbose_name = _('чек'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
