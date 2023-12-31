from random import choices
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.urls import reverse

from shopapp.utils import add_two_numbers
from shopapp.models import Product, Order


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)


class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')
        permission = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product_name = ''.join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()


    def test_create_product(self):
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name': self.product_name,
                'price': '123.45',
                'description': 'A good table',
                'discount': '10',

            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )


class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')
        cls.product = Product.objects.create(name='Best Product', created_by=cls.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_check_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)


class ProductsListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    fixtures = [
        'products-fixtures.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        expected_qs = Product.objects.filter(archived=False).all()
        result_qs = response.context['products']
        self.assertQuerySetEqual(
            expected_qs,
            result_qs,
            transform=lambda p: p.pk
        )
        # self.assertQuerySetEqual(
        #     qr=Product.objects.filter(archived=False).all(),
        #     value=(p.pk for p in response.context['products']),
        #     transform=lambda p: p.pk
        # )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')


class OrdersListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(response, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse('shopapp:orders_list'))
        self.assertRedirects(response, str(settings.LOGIN_URL)+'?next=/shop/orders/')


class ProductExportViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='bob_test', password='qwerty')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    fixtures = [
        'products-fixtures.json',
    ]

    def test_get_product_view(self):
        response = self.client.get(
            reverse('shopapp:products_export')
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': product.pk,
                'name': product.name,
                'price': str(product.price),
                'archived': product.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        permission = Permission.objects.filter(codename__in=['add_order', 'add_product', 'view_order'])
        cls.user.user_permissions.set(permission)
        cls.product = Product.objects.create(name='Test Product', price=10, created_by=cls.user)
        cls.order = Order.objects.create(
            user=cls.user,
            delivery_address='Test Address',
            promocode='TEST123'
        )
        cls.order.products.add(cls.product)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.order.delete()
        cls.product.delete()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_details(self):
        response = self.client.get(
            reverse('shopapp:order_details', kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['object'], self.order)


class OrdersExportViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            is_staff=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_orders_export(self):
        response = self.client.get(
            reverse('shopapp:orders_export')
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.id for product in order.products.all()]
            }
            for order in orders
        ]
        self.assertListEqual(response.json()['orders'], expected_data)
