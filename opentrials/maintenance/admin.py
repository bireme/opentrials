from django.contrib import admin
from maintenance import models
from utilities import safe_truncate
from datetime import datetime

def end_maintenance_window(modeladmin, request, queryset):
    queryset.update(actual_end=datetime.now())
end_maintenance_window.short_description = 'Mark selected maintenance window as ended'

class MaintenanceWindowAdmin(admin.ModelAdmin):
    list_display = ['short_description', 'start', 'estimated_end', 'actual_end', 'ended']
    actions = [end_maintenance_window]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.responsible = request.user
        obj.save()

    def short_description(self, obj):
        return safe_truncate(obj.description, 60)


admin.site.register(models.MaintenanceWindow, MaintenanceWindowAdmin)