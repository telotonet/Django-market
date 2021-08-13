from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from .models import Guest
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form          = UserAdminChangeForm   # Update users info
    add_form      = UserAdminCreationForm # Create new users
    
    list_display  = ('email', 'admin')
    list_filter   = ('admin',)
    fieldsets     = ( 
        ('Main Info', {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', )}),
        ('Permissions', {'fields': ('admin', 'active', 'staff')}),
    )  # Update users info
    add_fieldsets = (
        ("Create a new user", {'classes': ('wide', ),
                'fields': ('email', 'password1', 'password2')}),
    )  # Create new users
    search_fields = ('email', 'full_name',)
    ordering      = ('email', )
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class GuestAdmin(admin.ModelAdmin):
    search_fields = ['email', ]
    class Meta:
        model = Guest
        
admin.site.register(Guest, GuestAdmin)