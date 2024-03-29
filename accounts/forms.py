from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model   
from .models import EmailActivation
from django.contrib.auth.forms import ReadOnlyPasswordHashField # Скрытый пароль
from django.urls import reverse
from django.utils.safestring import mark_safe


User = get_user_model()


class ReactivateForm(forms.Form):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg = "This email does not exists, would you like to <a href='{register_link}'>register?</a>"
            return ValidationError(mark_safe(msg))
        return email
    
    

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin', 'full_name')
    
    def clean_password(self):
        return self.initial['password']

class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                'class':'form-control', 'name':'email', 'placeholder':'Email'}))

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match!")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise ValidationError('Email exists.')
        return email
    
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password !=password2:
            raise ValidationError('Passwords not much.')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False # send confirmation email via signals
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation_email()
        if commit:
            user.save()
        return user   
    

