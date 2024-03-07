from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(NewUser)
class MyUserAdmin(UserAdmin):
        model = NewUser
        list_display = ('username', 'email', 'code')
        list_filter = ('username', 'email')
        search_fields = ('username', )
        ordering = ('username', )
        filter_horizontal = ()
        fieldsets = (
                (None, {'fields': ('username', 'email', 'stripe_id', 'code', 'secondary_code', 'balance', 'clicks', 'sales')}),
                ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        )
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'code'),
            }),
    )
        
admin.site.register(Email)