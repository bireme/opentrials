from django.contrib import admin
from django.utils.safestring import mark_safe

from settings import PROJECT_PATH
from utilities import safe_truncate
from reviewapp.models import Submission, RecruitmentCountry, Remark, News, Attachment

class AdminFileLinkWidget(admin.widgets.AdminFileWidget):
    """
    A FileLinkField Widget that shows only the link to the file.
    """
    def __init__(self, attrs={}):
        super(AdminFileLinkWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append('<a target="_blank" href="%s">%s</a>' % \
                           (value.url.replace(PROJECT_PATH, u''), \
                            value.url.replace(PROJECT_PATH, u'').split("/")[-1], \
                           ))
        return mark_safe(u''.join(output))

class RecruitmentCountryInline(admin.TabularInline):
    model = RecruitmentCountry
    
class AttachmentInline(admin.TabularInline):
    model = Attachment
    fields = ('file',)
    can_delete = False
    max_num = 0
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'file':
            kwargs['widget'] = AdminFileLinkWidget
        return super(AttachmentInline, self).formfield_for_dbfield(db_field,**kwargs)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('creator_username', 'short_title', 'status')
    list_display_links = list_display
    list_filter = ('status',)
    date_hierarchy = 'updated'
    save_on_top = True
    change_form_template = 'admin/submission_change_form.html'
    inlines = [RecruitmentCountryInline, AttachmentInline]
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
        
if Submission not in admin.site._registry:
    admin.site.register(Submission, SubmissionAdmin)

if Remark not in admin.site._registry:
    admin.site.register(Remark, RemarkAdmin)

if News not in admin.site._registry:
    admin.site.register(News, NewsAdmin)
