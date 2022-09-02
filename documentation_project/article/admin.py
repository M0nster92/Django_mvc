from django.contrib import admin

from article.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display= ['name']

admin.site.register(Article, ArticleAdmin)