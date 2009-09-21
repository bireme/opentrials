#!/usr/bin/env python
from django.contrib import admin
from clinicaltrials.registry.models import ClinicalTrial, RecruitmentStatus
from clinicaltrials.registry.models import RecruitmentCountry

class RecruitmentCountryInline(admin.TabularInline):
    model = RecruitmentCountry
    
class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = [RecruitmentCountryInline]
    list_display = ('identifier', 'short_title', 'recruitment_status')
   
class RecruitmentStatusAdmin(admin.ModelAdmin):
    list_display = ('label', 'description')

admin.site.register( ClinicalTrial, ClinicalTrialAdmin )
admin.site.register( RecruitmentStatus, RecruitmentStatusAdmin )