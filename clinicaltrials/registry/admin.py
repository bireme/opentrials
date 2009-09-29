#!/usr/bin/env python
from django.contrib import admin
from registry.models import *

class RecruitmentCountryInline(admin.TabularInline):
    model = RecruitmentCountry

class OutcomeInline(admin.StackedInline):
    model = Outcome
    
class SecondaryNumberInline(admin.TabularInline):
    model = TrialNumber

class TrialInstitutionInline(admin.TabularInline):
    model = TrialInstitution
    
    
class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = [SecondaryNumberInline, RecruitmentCountryInline, 
               OutcomeInline, TrialInstitutionInline]
    list_display = ('updated_str','identifier','short_title','record_status',)
    list_display_links = ('identifier','short_title',)
    list_filter = ('record_status','study_type','phase',
                   'recruitment_status',)
    search_fields = ('scientific_title', 'public_title', 'i_freetext',)
              
admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
admin.site.register(Contact)
