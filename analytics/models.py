from django.db import models
from django.conf import settings 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from django.utils.translation import activate

from .signals import object_viewed_signal
from .utils import get_client_ip
from accounts.signals import user_logged_in


User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user           = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address     = models.CharField(max_length=220, blank=True, null=True) # IP Field
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField() # Instance ID
    content_object = GenericForeignKey('content_type', 'object_id') # Model instance
    timestamp      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_object} viewed on {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp', ]
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'
        

def objects_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    
    user = None
    if request.user.is_authenticated:
        user = request.user
        
    new_view_obj = ObjectViewed.objects.create(
        user         = user,
        content_type = c_type,
        object_id    = instance.id,
        ip_address   = get_client_ip(request),
    )
object_viewed_signal.connect(objects_viewed_receiver)



class UserSession(models.Model):
    user           = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ip_address     = models.CharField(max_length=220, blank=True, null=True) # IP Field
    session_key    = models.CharField(max_length=100, null=True, blank=True)
    timestamp      = models.DateTimeField(auto_now_add=True)
    active         = models.BooleanField(default=True)
    ended          = models.BooleanField(default=False)
    
    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended  = True
            self.save()
        except:
            pass
        return self.ended

# Деактивация предыдущих сессий

def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user=instance.user).exclude(id=instance.id)
        for el in qs:
            el.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()
            
post_save.connect(post_save_session_receiver, sender=UserSession)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    # print(instance)
    session_key = request.session.session_key
    ip_addres = get_client_ip(request)
    UserSession.objects.create(user=instance, ip_address=ip_addres, session_key=session_key)
    
user_logged_in.connect(user_logged_in_receiver)