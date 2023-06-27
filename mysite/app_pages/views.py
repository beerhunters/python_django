from time import sleep

from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(30)
def welcome(request, *args, **kwargs):
    sleep(4)
    return render(request, 'welcome.html')


def main_page(request, *args, **kwargs):
    return render(request, 'main_page.html')
