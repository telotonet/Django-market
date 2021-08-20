from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import  MarketingPreferenceForm
from django.contrib.messages.views import SuccessMessageMixin
from .models import MarketingPreference
from django.views.generic import UpdateView, View
from django.conf import settings
from .utils import Mailchimp
from .mixins import CsrfExemptMixin

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class      = MarketingPreferenceForm
    template_name   = 'base/forms.html'
    success_url     = '/settings/email/'
    success_message = 'Your email Preferences have been updated.'
    
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/settings/email/')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context          = super().get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context
    
    def get_object(self):
        user         = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj
    
    
    
    
    
    
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID', '1815fe83c0')
    

class MailchimpWebhookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        data    = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            type    = data.get('type')
            email   = data.get('data[email]')
            response_status_code, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = False
            mailchimp_subbed = False
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)

            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed  =is_subbed, 
                            mailchimp_subscribed  =mailchimp_subbed, 
                            mailchimp_msg  =str(data),
                        )
                
        return HttpResponse("Thank you", status=200)