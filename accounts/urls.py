from django.urls import path
from django.conf.urls import url
from .views import AccountHomeView, AccountActivateView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', AccountHomeView.as_view(), name='classhome'),
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountActivateView.as_view(), name='email-activate')
    # path('home/', account_home_view, name='funchome'),
]
