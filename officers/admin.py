from django.contrib import admin
from .models import Officer

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('get_user_first_name', 'get_user_email', 'specialization', 'workplace', 'experience')
    list_filter = ('specialization', 'workplace', 'is_verified')
    
    def get_user_first_name(self, obj):
        return obj.user.first_name
    
    def get_user_email(self, obj):
        return obj.user.email

admin.site.register(Officer, OfficerAdmin)