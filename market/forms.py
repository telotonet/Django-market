from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'name':'fullname', 'placeholder':'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'name':'email', 'placeholder':'Email'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'name':'content', 'placeholder':'Your content'}))
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if not "gmail.com" in email:
            raise ValidationError("your email must be gmail.com")

        return email

    
    
    