from django.urls import path
from blogapp.views import ArticleListView, ArticleDetailView, LatestArticleFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticleFeed(), name='article_feed'),
]