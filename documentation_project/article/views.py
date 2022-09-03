from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_list_or_404
from django.urls import is_valid_path, reverse
from django.contrib.auth.decorators import login_required

from article.models import Article
from .forms import ArticleForm

# Create your views here.
def index_view(request):
    articles = Article.objects.all()
    return render(request, template_name='index-view.html', context={'articles':articles})

@login_required
def article_create_view(request):
    form = ArticleForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            content = form.cleaned_data.get('content')
            article = Article.objects.create(name=name, content=content)
            print(article.id)
            return HttpResponseRedirect(reverse('article:article_detail', args=(article.id,)))
    return render(request, template_name='articles/create.html', context=context)

def article_detail_view(request, id=None):
    if id is not None:
        article = Article.objects.get(id=id)
    return render(request, template_name='articles/detail.html', context={'article': article})

def article_search_view(request):
    query = request.GET.get('query')
    article = None
    if query:
        article = Article.objects.get(id=query)
    context = {
        'article':article
    }
    return render(request, template_name='articles/search.html', context=context)