from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(NewUser)
class MyUserAdmin(UserAdmin):
        model = NewUser
        list_display = ('user_name', 'email', 'code')
        list_filter = ('user_name', 'email')
        search_fields = ('user_name', )
        ordering = ('user_name', )
        filter_horizontal = ()
        fieldsets = (
                (None, {'fields': ('user_name', 'email', 'code', 'balance')}),
                ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('user_name', 'password1', 'password2', 'code'),
            }),
    )
        
admin.site.register(Email)