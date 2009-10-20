from django.contrib import admin

from rebrac.models import Submission

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('creator_username', 'short_title', 'status')
    list_display_links = list_display
    list_filter = ('status',)
    date_hierarchy = 'updated'
    save_on_top = True
    change_form_template = 'admin/submission_change_form.html'
    def save_model(self, request, instance, form, change):
        if change:
            instance.updater = request.user
        else: # new submission
            instance.creator = request.user
        super(SubmissionAdmin, self).save_model(request, instance, form, change)

admin.site.register(Submission, SubmissionAdmin)
