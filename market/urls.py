
from os                         import name
from django.urls                import path, include
from django.conf                import settings
from django.conf.urls.static    import static
from django.contrib             import admin
from django.contrib.auth.views  import LogoutView



from .views             import home_page, about_page, contact_page
from addresses.views    import checkout_address_create_view, checkout_address_reuse_view
from accounts.views     import LoginView, RegisterView, guest_login_view
from carts.views        import cart_detail_api_view
from billing.views      import payment_method_view, payment_method_create_view
from marketing.views    import MarketingPreferenceUpdateView, MailchimpWebhookView

urlpatterns = [
    
      

    path('',            home_page, name='home'),
    path('payment/',    payment_method_view, name='payment'),
    path('payment/create/', payment_method_create_view, name='payment_create'),
    path('register/guest/', guest_login_view, name='guest_register'),
    path('api/cart/',   cart_detail_api_view, name='cart_detail_api'),
    path('logout/',     LogoutView.as_view(), name='logout'),
    path('products/',   include('products.urls')),
    path('search/',     include('search.urls')),
    path('cart/',       include('carts.urls')),
    path('settings/email/',             MarketingPreferenceUpdateView.as_view(), name='email'),
    path('webhooks/mailchimp/',         MailchimpWebhookView.as_view(), name='webohook'),
    path('checkout/address/reuse/',     checkout_address_reuse_view, name='reuse_address'),
    path('checkout/address/create/',    checkout_address_create_view, name='address'),
    path('login/',      LoginView.as_view(), name='login'),
    path('register/',   RegisterView.as_view(), name='register'),
    path('about/',      about_page, name='about'),
    path('contact/',    contact_page, name='contact'),
    path('admin/',      admin.site.urls),
    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)