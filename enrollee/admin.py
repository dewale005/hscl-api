from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from . import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'phone_no']
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'phone_no')}), 
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ), 
        (_('important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {'classes': ('wide', ), 'fields': ('email', 'first_name', 'last_name', 'phone_no', 'password1', 'password2')}),
    )

# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Enrollee)