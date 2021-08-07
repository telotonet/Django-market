from django.db import models
import random
import os
from django.db.models import Q
from django.http.response import Http404
from django.urls.base import reverse
from market.utils import unique_slug_generator
from django.db.models.signals import pre_save


def get_filename_ext(filepath):
    base_name   = os.path.basename(filepath)
    name, ext   = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):

    new_filename    = random.randint(1,23326662)
    name, ext       = get_filename_ext(filename)
    final_filename  = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}'

# Create your models here.

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True)
        

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def all(self):
        return self.get_queryset().active()
    
    def featured(self):
        return self.get_queryset().featured()

class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    image       = models.ImageField(upload_to=upload_image_path, null=True)
    featured    = models.BooleanField(default=False)
    active      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True, null=True)
    objects     = ProductManager()
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'slug': self.slug})
    
    
    def __str__(self) -> str: 
        return self.title
    def __unicode__(self) -> str:
        return self.title
    
    
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)
    
    
    
    
    