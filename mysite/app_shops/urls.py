from django.urls import path

from app_shops.views import page_with_cache_fragments

urlpatterns = [
    path('', page_with_cache_fragments, name='page_with_cache_fragments'),
]