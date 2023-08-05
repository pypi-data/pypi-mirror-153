import datetime
from django.contrib import admin
from .models import CMS
import time
admin.site.site_header = "Administration"
admin.site.index_title = "Administration" 
from django.utils.safestring import mark_safe

@admin.register(CMS)
class CMSAdmin(admin.ModelAdmin):
    list_display = ('title','slug','Created_at','Updated_at','thumb')
    readonly_fields = ('Created_at', 'Updated_at','slug')
    exclude = ('created_by','updated_by','created_at','updated_at')
    # fieldsets = (
    #     (None, {
    #         'fields': ('title','content') 
    #         } ),
    #           )
    def Created_at(self,obj):
        return mark_safe('%s' % datetime.datetime.fromtimestamp(obj.created_at))
    def Updated_at(self,obj):
        return mark_safe('%s' % datetime.datetime.fromtimestamp(obj.updated_at))
    def thumb(self, obj):
        pk=obj.pk
        return mark_safe('<div><a href="/admin/CMS/cms/%s/change/"><i class="fas fa-eye"></div>' % (obj.pk))
    thumb.allow_tags = True
    thumb.short_description = 'Details'
  
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
            obj.created_at = int(time.time())
        #if getattr(obj, 'updated_by', None) is None:
        obj.updated_by = request.user
        obj.updated_at = int(time.time())
        obj.save()
