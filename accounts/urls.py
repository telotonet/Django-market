from django.urls import path
from .views import AccountHomeView, account_home_view

urlpatterns = [
    path('', AccountHomeView.as_view(), name='classhome'),
    path('home/', account_home_view, name='funchome'),
]