from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'contact', 'housing_list', 'news_list']

    def location(self, item):
        return reverse(item)

class NewsSitemap(Sitemap):
    def items(self):
        return News.objects.all()

    def lastmod(self, obj):
        return obj.date