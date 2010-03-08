#!/usr/bin/env python

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings

from vocabulary.models import *

TARGET_LANG_CHECKS = tuple('translation_'+value for value, label
                           in settings.TARGET_LANGUAGES)

class VocabularyTranslationInline(generic.GenericTabularInline):
    model = VocabularyTranslation

class SimpleVocabularyAdmin(admin.ModelAdmin):
    list_display = ('label', 'description',) # + TARGET_LANG_CHECKS
    inlines = [VocabularyTranslationInline]

class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'language')
    search_fields = ('label', 'description')
    inlines = [VocabularyTranslationInline]

for model in (RecruitmentStatus, StudyType, StudyPhase, InterventionCode,
    AttachmentType, TrialNumberIssuingAuthority,
    StudyPurpose, InterventionAssigment, StudyMasking, StudyAllocation):
    admin.site.register(model, SimpleVocabularyAdmin)

admin.site.register(CountryCode, CountryCodeAdmin)
