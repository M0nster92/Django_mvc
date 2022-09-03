from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/already-logged-in.html', {})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error':'Invalid username or password'}
            return render(request, 'accounts/login.html', context)
        login(request, user)
        #return redirect('/')
        return redirect(request.GET.get('next'))

    return render(request, 'accounts/login.html', {})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login/')
    return render(request, 'accounts/logout.html', {})

def register_view(request):
    return render(request, 'accounts/register.html', {})