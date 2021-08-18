from django.contrib import admin
from .models import MarketingPreference

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display    = ['__str__', 'mailchimp_subscribed', 'updated']
    readonly_fields = ['mailchimp_subscribed', 'timestamp', 'updated', 'mailchimp_msg']
    class Meta:
        model = MarketingPreference
        fields = ['user', 'subscribed', 'mailchimp_msg']

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
# Register your models here.
