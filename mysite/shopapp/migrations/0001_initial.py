# Generated by Django 4.2.1 on 2023-05-19 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shopapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('discount', models.SmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('preview', models.ImageField(blank=True, null=True, upload_to=shopapp.models.product_preview_directory_path)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=shopapp.models.product_images_directory_path)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shopapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.TextField(blank=True, null=True)),
                ('promocode', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receipt', models.FileField(null=True, upload_to='orders/receipts')),
                ('products', models.ManyToManyField(related_name='orders', to='shopapp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
