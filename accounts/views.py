from django.shortcuts import render
from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import Guest

def guest_login_view(request):
    form = GuestForm(request.POST or None)
    context = {'form':form}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form.is_valid():
        email    = form.cleaned_data.get('email')
        new_guest = Guest.objects.create(email=email)
        request.session['guest'] = new_guest.pk
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('register')
    return redirect('register')

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {'form':form}
    next_get = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_get or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            try:
                del request.session['guest']
            except:
                pass
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
    return render(request, "accounts/login.html", context )

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {'form':form}
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username , email, password)
    return render(request, "accounts/register.html", context)
