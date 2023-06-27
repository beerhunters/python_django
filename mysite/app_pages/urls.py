from django.urls import path
from django.views.decorators.cache import cache_page

from app_pages.views import welcome, main_page

urlpatterns = [
    path('welcome', welcome, name='welcome'),
    path('main_page', cache_page(30)(main_page), name='main_page'),
]