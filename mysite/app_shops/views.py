from django.shortcuts import render

from app_shops.models import Shop


def page_with_cache_fragments(request):
    shops = Shop.objects.all()
    return render(request, 'app_shops/page_with_cache_fragments.html', context={'shops': shops})