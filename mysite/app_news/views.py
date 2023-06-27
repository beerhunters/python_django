from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core import serializers
from django.views.generic import DetailView

from app_news.models import NewsItem


def get_news_in_custom_format(request):
    format = request.GET['format']
    if format not in ['json', 'xml', 'yaml']:
        return HttpResponseBadRequest()
    data = serializers.serialize(format, NewsItem.objects.all())
    return HttpResponse(data)

class NewsItemDetailView(DetailView):
    model = NewsItem
    template_name = 'app_news/newsitem_details.html'