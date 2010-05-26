from django.contrib import admin
from utilities import safe_truncate
from reviewapp.models import Submission, RecruitmentCountry, Remark, News

class RecruitmentCountryInline(admin.TabularInline):
    model = RecruitmentCountry

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('creator_username', 'short_title', 'status')
    list_display_links = list_display
    list_filter = ('status',)
    date_hierarchy = 'updated'
    save_on_top = True
    change_form_template = 'admin/submission_change_form.html'
    inlines = [RecruitmentCountryInline]
    def save_model(self, request, instance, form, change):
        if change:
            instance.updater = request.user
        else: # new submission
            instance.creator = request.user
        super(SubmissionAdmin, self).save_model(request, instance, form, change)
        
class RemarkAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'context', 'short_text', 'verified', 'status')
    list_display_links = ('__unicode__', 'context', 'status')

    def save_model(self, request, instance, form, change):
        if not change:
            instance.creator = request.user
        super(RemarkAdmin, self).save_model(request, instance, form, change)
    
    
    def verified(self, obj):
        return obj.status == 'verified'
    verified.boolean = True
    
    def short_text(self, obj):
        return safe_truncate(obj.text)
        
class NewsAdmin(admin.ModelAdmin):

    list_display = ('__unicode__', 'short_text', 'created', 'creator', 'status')
    list_display_links = ('__unicode__', 'status')
    list_filter = ('created', 'status',)
    
    def save_model(self, request, instance, form, change):
        if not change:
            instance.creator = request.user
        super(NewsAdmin, self).save_model(request, instance, form, change)
        

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Remark, RemarkAdmin)
admin.site.register(News, NewsAdmin)
