from django.contrib import admin
from assistance.models import *
from utilities import safe_truncate, export_json

from polyglot.admin import TranslationInline, TranslationAdmin

class FieldHelpTranslationInline(TranslationInline):
    model = FieldHelpTranslation

class FieldHelpAdmin(TranslationAdmin):
    list_display = ('form','field','short_text',
                    'translation_completed', 'missing_translations')
    list_display_links = ('form','field')
    search_fields = ('form','field')
    list_filter = ('form',)
    inlines = [FieldHelpTranslationInline]
    actions = [export_json]

    def short_text(self, obj):
        return safe_truncate(obj.text)

class CategoryTranslationInline(TranslationInline):
    model = CategoryTranslation

class CategoryAdmin(TranslationAdmin):
    inlines = [CategoryTranslationInline]
    list_display = ('label',
                    'translation_completed', 'missing_translations')
    actions = [export_json]

class QuestionTranslationInline(TranslationInline):
    model = QuestionTranslation

class QuestionAdmin(TranslationAdmin):
    inlines = [QuestionTranslationInline]
    list_display = ('title','short_text',
                    'translation_completed', 'missing_translations')
    actions = [export_json]

    def short_text(self, obj):
        return safe_truncate(obj.answer)

if FieldHelp not in admin.site._registry:
    admin.site.register(FieldHelp, FieldHelpAdmin)

if Category not in admin.site._registry:
    admin.site.register(Category, CategoryAdmin)

if Question not in admin.site._registry:
    admin.site.register(Question, QuestionAdmin)