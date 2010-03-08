#!/usr/bin/env python
from django.contrib import admin
from vocabulary.models import *

class SimpleVocabularyAdmin(admin.ModelAdmin):
    list_display = ('label', 'description',)

class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'language')
    search_fields = ('label', 'description')

for model in (RecruitmentStatus, StudyType, StudyPhase, InterventionCode,
    AttachmentType, TrialNumberIssuingAuthority,
    StudyPurpose, InterventionAssigment, StudyMasking, StudyAllocation):
    admin.site.register(model, SimpleVocabularyAdmin)

admin.site.register(CountryCode, CountryCodeAdmin)
