from django.db import models

from market.utils import unique_order_id_generator
from carts.models import Cart
from addresses.models import Address
from math import fsum
from billing.models import BillingProfile
from django.db.models.signals import pre_save, post_save

ORDER_STATUS_CHOICES = (
    ( 'created' , 'Created' ),
    (    'paid' , 'Paid'    ),
    ( 'shipped' , 'Shipped' ),
    ('refunded' , 'Refunded'),
)

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
            created = False
        else:
            obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model): 
    
    cart                = models.ForeignKey(Cart, on_delete=models.CASCADE)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    shipping_address    = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True, related_name='shipping_address')
    billing_address     = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True, related_name='billing_address')
    
    active         = models.BooleanField(default=True)
    order_id       = models.CharField(max_length=120, blank=True)
    status         = models.CharField(max_length=120, default = 'created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=12, decimal_places = 2)
    total          = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    
    objects = OrderManager()
    
    def __str__(self) -> str:
        return self.order_id
    
    def update_total(self):
        cart_total      = self.cart.total
        shipping_total  = self.shipping_total
        new_total       = fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total      = formatted_total
        self.save()
        return new_total
    
    def check_done(self):
        billing_profile  = self.billing_profile
        shipping_address = self.shipping_address
        billing_address  = self.billing_address
        total            = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False
            
    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
        return self.status
        

def pre_save_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)
        
pre_save.connect(pre_save_order_id, sender=Order)

    
def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj   = instance
        cart_id    = cart_obj.pk
        qs         = Order.objects.filter(cart__pk=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
    
post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order_total, sender=Order)
