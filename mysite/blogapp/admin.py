from django.contrib import admin

from blogapp.models import Author, Category, Tag, Article

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)