from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model   
from django.forms import fields 

from django.contrib.auth.forms import ReadOnlyPasswordHashField # Скрытый пароль



User = get_user_model()

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
        fields = ('email', 'password', 'active', 'admin', 'full_name')
    
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
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user   
    
    