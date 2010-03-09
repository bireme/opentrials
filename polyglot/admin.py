from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings

from polyglot.models import Translation

class TranslationInline(generic.GenericStackedInline):
    max_num = len(settings.TARGET_LANGUAGES)
    radio_fields = {'language': admin.HORIZONTAL}

class TranslationAdmin(admin.ModelAdmin):
    def missing_translations(self, obj):
        return ' '.join(sorted(Translation.missing(obj)))

    def translation_completed(self, obj):
        return len(Translation.missing(obj)) == 0
    translation_completed.boolean = True
