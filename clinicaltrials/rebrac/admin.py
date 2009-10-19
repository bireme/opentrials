from django.contrib import admin
from rebrac.models import Submission
from registry.models import ClinicalTrial

from datetime import datetime

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('creator_username', 'short_title', 'status')
    list_display_links = list_display
    list_filter = ('status',)

    def save_model(self, request, instance, form, change):
        instance.updater = request.user
        if not change: # new submission
            instance.creator = request.user
        super(SubmissionAdmin, self).save_model(request, instance, form, change)

admin.site.register(Submission, SubmissionAdmin)
