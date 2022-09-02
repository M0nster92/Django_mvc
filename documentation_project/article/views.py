from django.http import HttpResponse
from django.shortcuts import render

from article.models import Article

# Create your views here.
def index_view(request):
    articles = Article.objects.all()
    return render(request, template_name='index-view.html', context={'articles':articles})

def article_home_view(request, id=None):
    if id is not None:
        article = Article.objects.get(id=id)
    return render(request, template_name='articles/detail.html', context={'article': article})