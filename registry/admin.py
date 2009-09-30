#!/usr/bin/env python
from django.contrib import admin
from registry.models import *

tabular_inline_models = [Descriptor, RecruitmentCountry, TrialInterventionCode,
                         TrialNumber, TrialContact, TrialInstitution]
tabular_inlines = []
for model in tabular_inline_models:
    cls_name = model.__name__+'line'
    cls = type(cls_name, (admin.TabularInline,), {'model':model})
    tabular_inlines.append(cls)

class OutcomeInline(admin.StackedInline):
    model = Outcome
       
class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = tabular_inlines + [OutcomeInline]
    list_display = ('updated_str','identifier','short_title','record_status',)
    list_display_links = ('identifier','short_title',)
    list_filter = ('record_status','study_type','phase',
                   'recruitment_status',)
    search_fields = ('scientific_title', 'public_title', 'i_freetext',)
              
admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
admin.site.register(Descriptor)
admin.site.register(Institution)
admin.site.register(Contact)
