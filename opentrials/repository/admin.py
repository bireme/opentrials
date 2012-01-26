# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.functional import update_wrapper
from django.http import HttpResponseRedirect
from django.db import models
from django.template.defaultfilters import yesno

from repository.models import *
from fossil.models import FossilIndexer

from polyglot.admin import TranslationInline, TranslationAdmin

tabular_inline_models = [Descriptor, TrialNumber, PublicContact, ScientificContact,
                         TrialSecondarySponsor, TrialSupportSource]
tabular_inlines = []
for model in tabular_inline_models:
    cls_name = model.__name__+'line'
    cls = type(cls_name, (admin.TabularInline,), {'model':model})
    tabular_inlines.append(cls)

class OutcomeInline(admin.StackedInline):
    model = Outcome

class ClinicalTrialTranslationInline(TranslationInline):
    model = ClinicalTrialTranslation

class ClinicalTrialAdmin(admin.ModelAdmin):
    inlines = tabular_inlines + [OutcomeInline, ClinicalTrialTranslationInline]
    list_display = ('updated_str','identifier','short_title','recruitment_status',)
    list_display_links = ('identifier','short_title',)
    search_fields = ('scientific_title', 'public_title', 'i_freetext',)
    list_filter = ('updated', 'study_type', 'phase', 'recruitment_status', 'status',)
    date_hierarchy = 'updated'
    save_on_top = True
    actions = ['publish_action']
    
    def publish_action(self, request, queryset):
        rows_updated = 0
        
        for obj in queryset:
            if obj.status != 'published':
                obj.status = 'published'
                obj.save()
                rows_updated += 1
                
        if rows_updated == 0:
            message = _("No clinical trial was published.") 
        elif rows_updated == 1:
            message = "1 %s" % _("clinical trial was published.")
        else:
            message = "%s %s" % (rows_updated, _("clinical trials were published."))
        self.message_user(request, message)

    publish_action.short_description = _("Publish the selected clinical trials")

class DescriptorAdmin(admin.ModelAdmin):
    list_display = ('trial_identifier','vocabulary','code', 'text')
    search_fields = ('code', 'text')
    list_filter = ('vocabulary', )

class InlineFossilIndexer(admin.TabularInline):
    model = FossilIndexer

class PublishedTrialAdmin(admin.ModelAdmin):
    list_display = ('display_text','creation','trial_id','is_most_recent','revision_sequential')
    list_filter = ('creation','is_most_recent','revision_sequential')
    search_fields = ('display_text','serialized')
    inlines = [InlineFossilIndexer]

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        default_urls = super(PublishedTrialAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns('',
                url(r'^(.+)/display-off/$', wrap(self.set_display_off), name='fossil_set_display_off'),
                url(r'^(.+)/display-on/$', wrap(self.set_display_on), name='fossil_set_display_on'),
                )
        
        return urlpatterns + default_urls

    def set_display_off(self, request, object_id):
        obj = self.get_object(request, object_id)
        obj.set_indexer('display', False)

        self.message_user(request, _('Published Trial set display to off.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

    def set_display_on(self, request, object_id):
        obj = self.get_object(request, object_id)
        obj.set_indexer('display', True)

        self.message_user(request, _('Published Trial set display to on.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '../'))

    def change_view(self, request, object_id, extra_context=None):
        if request.method == 'POST':
            self.message_user(request, _('This model is only for query porpuses.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER',
                reverse('admin:repository_publishedtrial_change', args=(object_id,))))

        fossil = self.get_object(request, object_id)

        extra_context = extra_context or {}
        extra_context['vocabulary_fields'] = ('study_type','purpose','intervention_assignment',
                'masking','allocation','recruitment_status','phase')
        extra_context['outcome_fields'] = ('primary_outcomes','secondary_outcomes')
        extra_context['description_fields'] = ('hc_code','hc_keyword','intervention_keyword')
        extra_context['trial_fields'] = []

        values_dict = fossil.trial.fossil.copy()

        # Ordinary fields
        for field in ClinicalTrial._meta.fields:
            if field.name in ('_deleted',):
                continue

            d_field = {
                'name': field.name,
                'label': field.verbose_name,
                }

            value = values_dict.pop(field.name, None)
           
            #print field.name, type(field)
            if isinstance(field, (models.BooleanField, models.NullBooleanField)):
                d_field['value'] = yesno(value)
            elif field.choices:
                d_field['value'] = dict(field.choices).get(value, value)
            else:
                d_field['value'] = value

            extra_context['trial_fields'].append(d_field)

        # Many to many fields
        for field in ClinicalTrial._meta.many_to_many:
            extra_context['trial_fields'].append({
                'name': field.name,
                'label': field.verbose_name,
                'value': values_dict.pop(field.name, None),
                })

        # Other children objects
        for name, value in values_dict.items():
            if name in ('__model__','scientific_acronym_display','acronym_display','pk',
                    '__unicode__','date_enrollment_start',):
                continue

            extra_context['trial_fields'].append({
                'name': name,
                'label': name,
                'value': values_dict.pop(name, None),
                })

        # Fossil meta fields
        extra_context['trial_fields'].append({
            'name': 'is_most_recent',
            'label': _('Is the most recent'),
            'value': yesno(fossil.is_most_recent),
            })
        extra_context['trial_fields'].append({
            'name': 'revision_sequential',
            'label': _('Revision Sequential'),
            'value': yesno(fossil.revision_sequential),
            })
        extra_context['trial_fields'].append({
            'name': 'status',
            'label': _('Status'),
            'value': fossil.status,
            })
        extra_context['trial_fields'].append({
            'name': 'display',
            'label': _('Displaying'),
            'value': yesno(fossil.display == 'True'),
            })

        return super(PublishedTrialAdmin, self).change_view(request, object_id, extra_context)

    def delete_view(self, request, object_id, extra_context=None):
        self.message_user(request, _('This model is only for query porpuses.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER',
            reverse('admin:repository_publishedtrial_change', args=(object_id,))))

    def add_view(self, request, form_url='', extra_context=None):
        self.message_user(request, _('This model is only for query porpuses.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER',
            reverse('admin:repository_publishedtrial_changelist')))

    def get_actions(self, request):
        return []

    def get_model_perms(self, request):
        perms = super(PublishedTrialAdmin, self).get_model_perms(request)
        perms['add'] = perms['delete'] = False
        
        return perms

class ContactAdmin(admin.ModelAdmin):
    list_filter = ('firstname', 'middlename', 'lastname', 'affiliation', 'email')
    search_fields = ('city', 'country')
    
class InstitutionAdmin(admin.ModelAdmin):
    list_filter = ('state', 'country', 'i_type')
    search_fields = ('name', )

if ClinicalTrial not in admin.site._registry:
    admin.site.register(ClinicalTrial, ClinicalTrialAdmin)

if Descriptor not in admin.site._registry:
    admin.site.register(Descriptor, DescriptorAdmin)

if Institution not in admin.site._registry:
    admin.site.register(Institution, InstitutionAdmin)

if Contact not in admin.site._registry:
    admin.site.register(Contact, ContactAdmin)

if PublishedTrial not in admin.site._registry:
    admin.site.register(PublishedTrial, PublishedTrialAdmin)

