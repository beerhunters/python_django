from django.contrib.sitemaps.views import sitemap
from django.urls import path

from housing.sitemap import StaticViewSitemap, NewsSitemap
from housing.views import home, about, contact, housing_list, news_list

sitemaps = {
    'static': StaticViewSitemap,
    'news': NewsSitemap
}

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('housing/', housing_list, name='housing_list'),
    path('news/', news_list, name='news_list'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]