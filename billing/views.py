from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .models import BillingProfile, Card
from django.conf import settings

import stripe

STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY', "sk_test_51JOQm5Faw5MMBhhdWTgtpl7aQMmxYoKGBfkK55Im9ePD7a0iL73SIEOmG80ghCP8Bb68273CRcvx6LdKlSMh1v2u00mjfLJdUG")
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY' ,"pk_test_51JOQm5Faw5MMBhhd20AkSufrvwbK47nk4WW3k489cWeAkKT5o42dqLdBa4YB7wltQio3RNDRznxvtBMaxT56g4Kd00eQX4tznK")
stripe.api_key = STRIPE_SECRET_KEY



def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('home')
    
    next_url = None
    next_get = request.GET.get('next')
    if is_safe_url(next_get, request.get_host()):
        next_url = next_get
    return render(request, 'billing/payment-method.html', {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url})

def payment_method_create_view(request):
    if request.method == 'POST' and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user!"}, status_code=401)
        token = request.POST.get('token')
        if token is not None:
            Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Your card was added."})
    return HttpResponse('error', status_code=401)