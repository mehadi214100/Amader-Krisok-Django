from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,UserProfile

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'is_staff', 'is_seller', 'is_farmer','is_officer')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_seller', 'is_farmer')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_farmer', 'is_seller', 'is_available','is_officer')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'phone_number', 'password1', 'password2'),
        }),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_name','gender','city')
    
    def get_name(self,obj):
        return obj.user.first_name

admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, ProfileAdmin)
