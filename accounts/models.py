from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.mail import send_mail
from django.template.loader import  get_template
from django.conf import settings



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

    
class EmailActivation(models.Model):        
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    email           = models.EmailField()
    key             = models.ChatField(max_length=120, blank=True, null=True)
    activated       = models.BooleanField(default=False)
    forced_expired  = models.BooleanField(default=False)
    expires         = models.IntegerField(default=7) # 7 Days
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
    def send_activation(self):
        context = {
            'path': "some_path_with_key",
            'email': self.email,  
        }
        txt_    = get_template("registration/emails/verify.txt").render(context)
        html_   = get_template("registration/emails/verify.html").render(context)
        
        subject = '1-Click Email Verification'
        
        sent_mail = send_mail(
            subject,
            message = txt_,
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            html_message = html_,
            fail_silently=False,
        )
        

class Guest(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    
