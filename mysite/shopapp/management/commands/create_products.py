from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    """
    Create Products
    """
    def handle(self, *args, **kwargs):
         self.stdout.write('Create products')
         products = [
             'Laptop',
             'Desktop',
             'Smartphone'
         ]
         for products_name in products:
             product, created = Product.objects.get_or_create(name=products_name)
             self.stdout.write(f'Created product {products_name}')
         self.stdout.write(self.style.SUCCESS('Product created successfully'))
