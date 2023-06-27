from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, DetailView
from .models import Article

class ArticleListView(ListView):
    model = Article
    queryset = Article.objects.select_related('author', 'category').prefetch_related('tags')
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'

class ArticleDetailView(DetailView):
    model = Article

class LatestArticleFeed(Feed):
    title = 'Latest Article'
    description = 'Upcoming articles'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return Article.objects.order_by('-pub_date')[:5]

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    # def item_link(self, item: Article):
    #     return reverse('blogapp:article', kwargs={'pk': item.pk})