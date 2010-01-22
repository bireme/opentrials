from django.contrib import admin
from assistance.models import *
from utilities import safe_truncate

class FieldHelpAdmin(admin.ModelAdmin):
    list_display = ('form','field','done','short_text')
    list_display_links = ('form','field')
    search_fields = ('form','field')
    list_filter = ('form',)
    
    def done(self, obj):
        return bool(obj.text.strip())
    done.boolean = True
    
    def short_text(self, obj):
        return safe_truncate(obj.text, 80)
    
        
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(FieldHelp, FieldHelpAdmin)