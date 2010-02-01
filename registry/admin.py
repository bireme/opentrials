# -*- coding: utf-8 -*-

from django.contrib import admin
from registry.models import *

tabular_inline_models = [Descriptor, TrialNumber, PublicContact, ScientificContact,
                         TrialSecondarySponsor, TrialSupportSource]
tabular_inlines = []
for model in tabular_inline_models:
    cls_name = model.__name__+'line'
    cls = type(cls_name, (admin.TabularInline,), {'model':model})
    tabular_inlines.append(cls)

class OutcomeInline(admin.StackedInline):
    model = Outcome

class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = tabular_inlines + [OutcomeInline]
    list_display = ('updated_str','identifier','short_title','recruitment_status',)
    list_display_links = ('identifier','short_title',)
    search_fields = ('scientific_title', 'public_title', 'i_freetext',)
    list_filter = ('updated', 'study_type', 'phase', 'recruitment_status',)
    date_hierarchy = 'updated'
    save_on_top = True

class DescriptorAdmin(admin.ModelAdmin):
    list_display = ('trial_identifier','vocabulary','code', 'text')

admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
admin.site.register(Descriptor, DescriptorAdmin)
admin.site.register(Institution)
admin.site.register(Contact)
