from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                'class':'form-control', 'name':'email', 'placeholder':'Email'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class RegisterForm(LoginForm, forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                'class':'form-control', 'name':'email', 'placeholder':'Email'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
                'class':'form-control'}))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise ValidationError('Username exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email = email)
        if qs.exists():
            raise ValidationError('Email exists.')
        return email
    
    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password !=password2:
            raise ValidationError('Passwords not much.')