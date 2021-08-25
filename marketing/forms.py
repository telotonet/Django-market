from django  import  forms
from .models import MarketingPreference

class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.CharField(label = 'Receive Marketing Email', required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed',
        ]
        
        