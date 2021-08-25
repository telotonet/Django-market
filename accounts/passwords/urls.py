from django.contrib.auth import views
from django.urls import path


urlpatterns = [
     
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    
    path('password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/\(<uidb64>[0-9A-Za-z_\-]+)/\(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     
]
