# coding: utf-8

from clinicaltrials.registry.models import TrialInstitution
from django import forms
from django.utils.translation import ugettext as _

from django.forms.formsets import formset_factory


class TrialIdentificationForm(forms.Form):
    title = _('Trial Identification')
    # TRDS 10a
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000, 
                                       widget=forms.Textarea)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=False,
                                         label=_('Scientific Acronym'),
                                         max_length=255)
    scientific_acronym_expansion = forms.CharField(required=False,
                                         label=_('Scientific Acronym Expansion'),
                                         max_length=255)
    # TRDS 9a
    public_title = forms.CharField(required=False, 
                                   label=_('Public Title'),
                                   max_length=2000, 
                                   widget=forms.Textarea)
    # TRDS 9b
    acronym = forms.CharField(required=False, label=_('Acronym'),
                              max_length=255)
    acronym_expansion = forms.CharField(required=False,
                                         label=_('Acronym Expansion'),
                                         max_length=255)

class TrialNumberForm(forms.Form):
    issuing_authority = forms.CharField(_('Issuing Authority'),
                                         max_length=255, db_index=True)
    id_number = forms.CharField(_('Secondary Id Number'))
                                 

                                 
