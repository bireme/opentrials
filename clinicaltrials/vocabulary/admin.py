#!/usr/bin/env python
from django.contrib import admin
from vocabulary.models import *

class SimpleVocabularyAdmin(admin.ModelAdmin):
    list_display = ('label', 'description',)

for model in (RecruitmentStatus, StudyType, StudyPhase, ):
    admin.site.register(model, SimpleVocabularyAdmin)
