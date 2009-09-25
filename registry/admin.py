#!/usr/bin/env python
from django.contrib import admin
from clinicaltrials.registry.models import *

class RecruitmentCountryInline(admin.TabularInline):
    model = RecruitmentCountry

class OutcomeInline(admin.StackedInline):
    model = Outcome
    
class SecondaryNumberInline(admin.TabularInline):
    model = TrialNumber
    
class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = [SecondaryNumberInline, RecruitmentCountryInline, 
               OutcomeInline]
    list_display = ('identifier', 'short_title', 'recruitment_status',)
       
class SimpleVocabularyAdmin(admin.ModelAdmin):
    list_display = ('label', 'description',)

admin.site.register(ClinicalTrial, ClinicalTrialAdmin)
admin.site.register(Institution)

for model in (RecruitmentStatus, StudyType, StudyPhase, ):
    admin.site.register(model, SimpleVocabularyAdmin)
