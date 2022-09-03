from django.urls import path

from . import views

app_name = 'article'
urlpatterns= [
    path('', views.index_view, name='article_index'),
    path('articles/', views.article_search_view, name='article_search_view'),
    path('article/create/', views.article_create_view, name='article_create_view'),
    path('article/<int:id>/', views.article_detail_view, name='article_detail'),
]