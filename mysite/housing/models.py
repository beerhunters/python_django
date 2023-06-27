from django.db import models

class Housing(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    description = models.TextField(verbose_name='описание')
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, related_name='housing', null=True, verbose_name='тип жилья')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='картинка')

    class Meta:
        verbose_name = 'жилье'
        verbose_name_plural = 'жилье'

    def __str__(self):
        return self.title

class RoomType(models.Model):
    title = models.CharField(max_length=50, verbose_name='тип жилья')

    class Meta:
        verbose_name = 'тип жилья'
        verbose_name_plural = 'типы жилья'

    def __str__(self):
        return self.title

class RoomCount(models.Model):
    count = models.IntegerField(verbose_name='количество комнат')

    class Meta:
        verbose_name = 'количество комнат'
        verbose_name_plural = 'количество комнат'

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    text = models.TextField(verbose_name='описание')
    date = models.DateField(auto_now_add=True, verbose_name='дата')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'

    def __str__(self):
        return self.title