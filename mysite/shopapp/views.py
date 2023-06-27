"""
В этом модуле лежать различные наборы представлений.

Разные view интернет-магазина: по заказам, товарам и т.д.
"""
from csv import DictWriter
from timeit import default_timer

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from shopapp.common import save_csv_products
from shopapp.forms import ProductForm, GroupForm
from shopapp.models import Product, Order, ProductImage
from shopapp.serializers import ProductSerializer, OrderSerializer


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived',
    ]
    ordering_fields = [
        'name',
        'price',
        'discount',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, returns 404 if not found',
        responses={
        200: ProductSerializer,
        404: OpenApiResponse(description='Empty response, product by ID not found'),
    }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        # print('hello')
        return super().list(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self,request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = ['name', 'description', 'price', 'discount']
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return

    @action(methods=['post'], detail=False, parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(request.FILES['file'].file, request.encoding)
        serializer = self.get_serializer(data=products, many=True)
        return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'delivery_address',
        'promocode',
        'user',
        'products',
    ]
    ordering_fields = [
        'created_at',
        'user',
    ]


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'items': 2,
        }
        print('shop index context:', context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     return self.request.user.is_superuser

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def get_success_url(self):
        return reverse('shopapp:product_details',
                       kwargs={'pk': self.object.pk})

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm('shopapp.change_product')
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class CreateOrderView(CreateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode', 'products'
    success_url = reverse_lazy('shopapp:orders_list')


class OrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/orders_list.html'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
    queryset = (Order.objects.
                select_related('user').
                prefetch_related('products'))


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'delivery_address', 'promocode', 'products'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('shopapp:order_details',
                       kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = 'products_data_export'
        prodcuts_data = cache.get(cache_key)
        if prodcuts_data is None:
            products = Product.objects.order_by('pk').all()
            products_data = [
                {
                    'pk': product.pk,
                    'name': product.name,
                    'price': product.price,
                    'archived': product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 300)
        elem = products_data[0]
        name = elem['name']
        print('name: %s' % name)
        return JsonResponse({'products': products_data})


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        orders = Order.objects.order_by('pk').all()
        data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.pk,
                'products': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]
        return JsonResponse({'orders': data})


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'shopapp/orders_list.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        self.owner = user
        queryset = super().get_queryset().filter(user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        if self.object_list:
            context['message'] = f"Пользователь {self.owner.username} выполнил следующие заказы:"
        else:
            context['message'] = f"У пользователя {self.owner.username} ещё нет заказов"
        return context


class UserOrdersExportView(View):
    def get(self, request, user_id):
        cache_key = f'user_orders_{user_id}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return JsonResponse(cached_data, safe=False)
        else:
            user = get_object_or_404(User, id=user_id)
            orders = Order.objects.filter(user=user).order_by('id')
            serializer = OrderSerializer(orders, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60)
            return JsonResponse(data, safe=False)