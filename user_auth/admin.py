from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sessions.models import Session

from .models import CustomUser, Role

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'full_name', 'user_role', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    readonly_fields = ['date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'user_role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'user_role', 'is_staff', 'is_superuser'),
        }),
    )

    ordering = ['email']
    filter_horizontal = ()

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = 'Full Name'

# Register the CustomUser model with the UserAdmin class
admin.site.register(CustomUser, UserAdmin)

# --------------------------------------------------------------
admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
# ---------------------------------------------------------------

@admin.register(Role)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')