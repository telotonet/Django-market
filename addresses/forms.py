from django import forms
from django.db import models
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        fields = ('address_line_1','address_line_2', 'city', 'country', 'state', 'postal_code')
        model = Address