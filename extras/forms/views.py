from django.shortcuts import redirect, render

from forms.models import Product, ProductPlus
from .forms import ContactForm, ProductForm, ProductPlusForm

# Create your views here.


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        print(form)

    form = ContactForm()
    return render(request, 'form.html', {'form': form})


def product_plus(request):
    if request.method == 'POST':
        form = ProductPlusForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('product_plus_list')

    form = ProductPlusForm()
    return render(request, 'form.html', {'form': form})


def product_plus_list(request):
    context = {
        'products': ProductPlus.objects.all()
    }

    return render(request, 'product_plus.html', context)


def create_product(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()

    form = ProductForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)


def product_list(request):
    context = {
        'products': Product.objects.all().prefetch_related('tag')
    }

    product = Product.objects.all().prefetch_related('tag')

    return render(request, 'product.html', context)


def product_update(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            return redirect('product_list')

    context = {
        'form': form
    }

    return render(request, 'product-update.html', context)
