from django.contrib import admin

from housing.models import Housing, RoomType, RoomCount, News

# class NewsItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title',)
#
#
# class NewsTypeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'code',)

admin.site.register(Housing)
admin.site.register(RoomType)
admin.site.register(RoomCount)
admin.site.register(News)
