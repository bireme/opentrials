#!/usr/bin/env python

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings

from vocabulary.models import *

TARGET_LANG_CHECKS = tuple('translation_'+value for value, label
                           in settings.TARGET_LANGUAGES)

class VocabularyTranslationInline(generic.GenericStackedInline):
    model = VocabularyTranslation
    max_num = len(settings.TARGET_LANGUAGES)
    radio_fields = {'language': admin.HORIZONTAL}

class SimpleVocabularyAdmin(admin.ModelAdmin):
    list_display = ('label', 'description', 'translation_completed', 'missing_translations')
    inlines = [VocabularyTranslationInline]

    def translation_completed(self, obj):
        return len(Translation.missing(obj)) == 0
    translation_completed.boolean = True

class CountryCodeAdmin(SimpleVocabularyAdmin):
    list_display = ('label', 'description', 'submission_language', 'translation_completed', 'missing_translations')
    search_fields = ('label', 'description')
    inlines = [VocabularyTranslationInline]

for model in (RecruitmentStatus, StudyType, StudyPhase, InterventionCode,
    AttachmentType, TrialNumberIssuingAuthority,
    StudyPurpose, InterventionAssigment, StudyMasking, StudyAllocation):
    admin.site.register(model, SimpleVocabularyAdmin)

admin.site.register(CountryCode, CountryCodeAdmin)
