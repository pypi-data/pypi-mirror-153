import datetime
from tabnanny import verbose
from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


# Register your models here.
class Settingsadmin(admin.ModelAdmin):
    list_display = ('key','values')
    readonly_fields = ('created_at','updated_at')
    # change_list_template='mobileversion.html'
admin.site.register(setting,Settingsadmin)

class mobile(setting):
    class Meta:
        proxy = True
        verbose_name='mobile Management'
class formobile(Settingsadmin):
    change_list_template='mobileversion.html'

admin.site.register(mobile,formobile)
class UserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    list_display = ('username', 'email','Created_at','Updated_at','thumbIsactive','thumb')
    readonly_fields = ('username', 'email','created_at','updated_at','is_actives','password','email_verified','is_actives','mobile','isd_code','last_login','local','first_name','last_name', 'date_joined','mobile_verified_at','mobile_verified','email_verified_at' )
    view_on_site = False
    search_fields = ['username','email',]
    list_per_page = 10
    list_filter = ('email',)
    def Created_at(self,obj):

         return mark_safe('%s' % datetime.datetime.fromtimestamp(obj.created_at))
    def Updated_at(self,obj):
         return mark_safe('%s' % datetime.datetime.fromtimestamp(obj.updated_at))
    def thumb(self, obj):
        pk=obj.pk
        return mark_safe('<div><a href="/admins/authentication/%s/%s"><i class="fas fa-eye"></div>' % ('user', obj.pk))
    thumb.allow_tags = True
    thumb.short_description = 'Details'

    def thumbIsactive(self,obj):    
        pk=obj.pk
        if obj.is_actives == True:
            return mark_safe('<button type="button" class="btn btn-primary btn-sm" id="myButton%s" onclick=activeInactive(%s)>active</button>'%(pk, pk))
        else:
            return mark_safe('<button type="button" class="btn btn-danger btn-sm" id="myButton%s" onclick=activeInactive(%s)>Inactive</button>'%(pk, pk))

            
    thumbIsactive.allow_tags = True
    thumbIsactive.short_description = 'Active'


admin.site.register(User,UserAdmin)
