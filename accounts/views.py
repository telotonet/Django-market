from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm, GuestForm, EmailActivation
from django.views.generic import CreateView, FormView, DetailView, View 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import is_safe_url
from .models import Guest
from .signals import user_logged_in
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.views.generic.edit import FormMixin
from .forms import ReactivateForm


class AccountHomeView(LoginRequiredMixin, DetailView):
    redirect_field_name = 'next'
    template_name       = 'accounts/home.html'
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
     
    def get_object(self):
        return self.request.user
    
    
class AccountActivateView(FormMixin, View):
    success_url = '/login/'
    form_class  = ReactivateForm
    key = None
    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            print(self.kwargs.get('key'))
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = f"Your email has already confirmed. \n Do you need to <a href='{reset_link}'> reset your password? </a>"
                    messages.success(request, format_html(msg))
                    return redirect('login')
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context) 

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        obj   = EmailActivation.objects.email_exists(email).first()
        if obj is not None:
            msg = """Activation link sent, please check yor email."""
            messages.success(request, msg)
            user = obj.user
            new_activation = EmailActivation.objects.create(user=user, email=email)
            new_activation.send_activation_email()
            return super().form_valid(form)
        else:
            register = reverse('register')
            msg = f"This email does not exists, would you like to <a href='{register}'> register? </a>"
            messages.warning(request, format_html(msg))
            return redirect('home')
    def form_invalid(self, form):
        request = self.request
        context = {'form': form}
        return render(request, 'registration/activation-error.html', context)


# @login_required(redirect_field_name='next')
# def account_home_view(request):
#     return render(request, "accounts/home.html", {})

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

class LoginView(FormView):
    form_class  = LoginForm
    success_url = '/'
    template_name = "accounts/login.html"
    def form_valid(self, form):
        request = self.request
        next_get = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_get or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username = email, password = password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Account is inactive")
                return super().form_invalid(form)
            try:
                del request.session['guest']
            except:
                pass
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
        return super().form_invalid(form)
    
class RegisterView(CreateView):
    form_class    = RegisterForm
    template_name = "accounts/register.html"
    success_url   = '/login/'


# User = get_user_model()
# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     context = {'form':form}
#     if form.is_valid():
#         form.save()
#     return render(request,"accounts/register.html" , context)
# def login_page(request):
#     form = LoginForm(request.POST or None)
#     context = {'form':form}
#     if form.is_valid():
#     return render(request, "accounts/login.html", context )