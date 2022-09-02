from django.urls import path

from . import views

app_name = 'article'
urlpatterns= [
    path('', views.index_view, name='article_index'),
    path('<int:id>/', views.article_home_view, name='article_home')
]