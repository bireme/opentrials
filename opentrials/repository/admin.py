# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from repository.models import *

from polyglot.admin import TranslationInline, TranslationAdmin

tabular_inline_models = [Descriptor, TrialNumber, PublicContact, ScientificContact,
                         TrialSecondarySponsor, TrialSupportSource]
tabular_inlines = []
for model in tabular_inline_models:
    cls_name = model.__name__+'line'
    cls = type(cls_name, (admin.TabularInline,), {'model':model})
    tabular_inlines.append(cls)

class OutcomeInline(admin.StackedInline):
    model = Outcome

class ClinicalTrialTranslationInline(TranslationInline):
    model = ClinicalTrialTranslation

class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = tabular_inlines + [OutcomeInline, ClinicalTrialTranslationInline]
    list_display = ('updated_str','identifier','short_title','recruitment_status',)
    list_display_links = ('identifier','short_title',)
    search_fields = ('scientific_title', 'public_title', 'i_freetext',)
    list_filter = ('updated', 'study_type', 'phase', 'recruitment_status', 'status',)
    date_hierarchy = 'updated'
    save_on_top = True
    actions = ['publish_action']
    
    def publish_action(self, request, queryset):
        rows_updated = 0
        
        for obj in queryset:
            if obj.status != 'published':
                obj.status = 'published'
                obj.save()
                rows_updated += 1
                
        if rows_updated == 0:
            message = _("No clinical trial was published.") 
        elif rows_updated == 1:
            message = "1 %s" % _("clinical trial was published.")
        else:
            message = "%s %s" % (rows_updated, _("clinical trials were published."))
        self.message_user(request, message)

    publish_action.short_description = _("Publish the selected clinical trials")

class DescriptorAdmin(admin.ModelAdmin):
    list_display = ('trial_identifier','vocabulary','code', 'text')

if ClinicalTrial not in admin.site._registry:
    admin.site.register(ClinicalTrial, ClinicalTrialAdmin)

if Descriptor not in admin.site._registry:
    admin.site.register(Descriptor, DescriptorAdmin)

if Institution not in admin.site._registry:
    admin.site.register(Institution)

if Contact not in admin.site._registry:
    admin.site.register(Contact)
