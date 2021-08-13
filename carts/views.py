from django.shortcuts import render, redirect
from .models import Cart
from django.http import JsonResponse
from accounts.models import Guest
from django.http.response import Http404
from products.models import Product
from addresses.forms import AddressForm
from orders.models import Order
from addresses.models import Address
from billing.models import BillingProfile
from accounts.forms import LoginForm, GuestForm



def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{'title': x.title, 'price': x.price, 'description': x.description, 'url': x.get_absolute_url(), 'id':x.pk} for x in cart_obj.products.all()]
    cart_data = {'products': products, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {'cart':cart_obj})

def cart_update(request):
    product_pk = request.POST.get('product_id')
    if product_pk is not None:
        try:
            product_obj = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return redirect('cart_home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                "added": added,
                'removed': not added,
                "cartItemCounter": cart_obj.products.count(),
            }
            return JsonResponse(json_data, status=200)
    return redirect('cart_home')
    

    
def checkout_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    order_obj         = None
    if new_obj or cart_obj.products.count==0:
        return redirect('cart_home')
    login_form           = LoginForm()
    guest_form           = GuestForm()
    address_form         = AddressForm()
    billing_address_id   = request.session.get('billing_address_id', None)
    shipping_address_id  = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs           = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(pk=shipping_address_id)
            del request.session['shipping_address_id']
        elif billing_address_id:
            order_obj.billing_address  = Address.objects.get(pk=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()
            
    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect('success')
        
    
    context = {
        "object":order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
    }
    return render(request, 'carts/checkout.html', context)



def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})