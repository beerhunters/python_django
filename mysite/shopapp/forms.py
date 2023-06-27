from django import forms
from django.contrib.auth.models import Group
from shopapp.models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": False})
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'user', 'delivery_address', 'promocode', 'products',


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()