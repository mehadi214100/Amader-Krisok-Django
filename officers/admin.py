from django.contrib import admin
from .models import Officer,OfficerBook

class OfficerAdmin(admin.ModelAdmin):
    list_display = ('get_user_first_name', 'get_user_email', 'specialization', 'workplace', 'experience')
    list_filter = ('specialization', 'workplace', 'is_available')
    
    def get_user_first_name(self, obj):
        return obj.user.first_name
    
    def get_user_email(self, obj):
        return obj.user.email


class officerBookAdmin(admin.ModelAdmin):
    list_display = ('get_user_first_name','get_officer_first_name','date','status')

    def get_user_first_name(self, obj):
        return obj.user.first_name
    
    def get_officer_first_name(self, obj):
        return obj.officer.user.first_name

admin.site.register(Officer, OfficerAdmin)
admin.site.register(OfficerBook,officerBookAdmin)