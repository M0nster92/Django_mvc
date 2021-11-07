from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import fields, inlineformset_factory
from .models import Product, Order, Customer
from .forms import CreateUserForm, OrderForm, UserCreationForm, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_ony


@login_required(login_url='login')
@admin_ony
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = Customer.objects.count()
    total_orders = Order.objects.count()
    delivered = Order.objects.filter(status='Delivered').count()
    pending = Order.objects.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customer': total_customer,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print(orders)
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    order_count = customer.order_set.count()

    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'filter': orderFilter
    }
    return render(request, 'accounts/customer.html', context)


@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    #OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    #formset = OrderFormSet(instance=customer)
    form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        #formset = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    content = {'item': order}
    return render(request, 'accounts/delete.html', content)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form': form
    }
    return render(request, 'accounts/account_settings.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            '''groups = user.groups.all()
            for group in groups:
                if group.name == 'admin':
                    print('success')
                else:
                    print('failed')'''
            # if 'admin' in groups:
            #   print(groups)
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username or passsword is incorrect')

    context = {}

    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
