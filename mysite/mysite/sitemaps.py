from app_news.sitemap import NewsSitemap
from blogapp.sitemap import BlogSitemap

sitemaps = {
    'blog': BlogSitemap,
    'news': NewsSitemap,
}