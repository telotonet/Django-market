from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import  get_template
from django.conf import settings
from django.utils.translation import activate
from market.utils import random_string_generator, unique_key_generator
from django.db.models.signals import post_save, pre_save

from django.utils import timezone


ACTIVATION_DAYS = getattr(settings, "ACTIVATION_DAYS", 7)

class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False,  is_admin=False):
        if not email:
            raise ValueError('Users must have email address!')
        if not password:
            raise ValueError('Users must have a password!')
        user_obj = self.model(email = self.normalize_email(email))
        user_obj.set_password(password)
        user_obj.staff     = is_staff
        user_obj.full_name = full_name
        user_obj.is_active = is_active
        user_obj.admin     = is_admin
        user_obj.save()
        return user_obj
    
    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email    =email,
            full_name=full_name,
            password =password,
            is_admin =True,
            is_staff =True,
        )
        return user
    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_admin=True,
        )
        return user
        
class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255,unique=True)
    full_name   = models.CharField(max_length=255, blank=True, null=True)
    is_active   = models.BooleanField(default=True) #can login
    staff       = models.BooleanField(default=False) # admin user
    admin       = models.BooleanField(default=False) # super user
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email' 
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email
    
    def get_short_name(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff
    
    # @property
    # def is_active(self):
    #     return self.active
    
    @property
    def is_admin(self):
        return self.admin

class Guest(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    
class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated      = False,
            forced_expired = False,
        ).filter(
            timestamp__gt  = start_range,
            timestamp__lte = end_range,
        )
    
    
class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)
    
    def confirmable(self):
        return self.get_queryset().confirmable()
    
    def email_exists(self, email):
        return self.get_queryset().filter(Q(email=email) | Q(user__email=email)).filter(activated=False)
    
    
    
class EmailActivation(models.Model):        
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.CharField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=ACTIVATION_DAYS)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    
    objects = EmailActivationManager()
    
    
    def __str__(self):
        return self.email
    
    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 obj
        if qs.exists():
            return True
        return False
    
    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False
                
    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False
    
    def send_activation_email(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url    = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
                key_path    = self.key
                path        = f"{base_url}/account/email/confirm/{key_path}/"
                
                context = {
                    "key": key_path,
                    'path': path,
                    'email': self.email,  
                }
                
                txt_    = get_template("registration/emails/verify.txt").render(context)
                html_   = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Verification'
                sent_mail = send_mail(
                    subject,
                    message = txt_,
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [self.email],
                    html_message = html_,
                    fail_silently=False,
                )
                return sent_mail
        False


def pre_save_email_activate_key(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activate_key, sender=EmailActivation)





            
def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation_email()

post_save.connect(post_save_user_create_receiver, sender=User)





    
