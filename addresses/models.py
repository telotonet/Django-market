from django.db import models
from billing.models import BillingProfile



ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type    = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, blank=True, null=True, default='')
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default = 'United States of America')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)
    
    def __str__(self) -> str:
        return str(self.billing_profile)
    
    def get_address(self):
        return f'{self.address_line_1}\n{self.address_line_2}\n{self.postal_code}\n{self.city}\n{self.state}\n{self.country}\n'