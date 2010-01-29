# coding: utf-8

from django import forms
from django.utils.translation import ugettext as _

#from django.contrib.admin.widgets import AdminDateWidget


from clinicaltrials.registry.models import ClinicalTrial

class TrialIdentificationForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['scientific_title','scientific_acronym',
                  'public_title','acronym']

    title = _('Trial Identification')
    # TRDS 10a
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000, 
                                       widget=forms.Textarea)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=False,
                                         label=_('Scientific Acronym'),
                                         max_length=255)
    # TRDS 10c
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

    # TODO: Secondary Numbers