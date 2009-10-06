# coding: utf-8

from django import forms
from django.utils.translation import ugettext as _

import choices

class TrialIdentificationForm(forms.Form):
    title = _('Trial Identifcation')
    # TRDS 10a
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=False, label=_('Scientific Acronym'), 
                                         max_length=255)
    # TRDS 9a
    public_title = forms.CharField(required=False, label=_('Public Title'), max_length=2000)
    # TRDS 9b
    acronym = forms.CharField(required=False, label=_('Acronym'), max_length=255)
    
    # TODO: Secondary Numbers
    
    
class RecruitmentForm(forms.Form):
    title = _('Recruitment')
    
    # TODO: Countries of Recruitment
    
    # TRDS 14a
    inclusion_criteria = forms.CharField(required=False, label=_('Inclusion Criteria'), 
                                          max_length=8000)
    # TRDS 14b
    gender = forms.ChoiceField(label=_('Gender (inclusion sex)'),
                               choices=choices.INCLUSION_GENDER)
    # TRDS 14c
    agemin_value = forms.IntegerField(required=False, label=_('Inclusion Minimum Age'))
                                      
    agemin_unit = forms.ChoiceField(label=_('Minimum Age Unit'), 
                                   choices=choices.INCLUSION_AGE_UNIT)
    # TRDS 14d
    agemax_value = forms.IntegerField(required=False, label=_('Inclusion Maximum Age'))
    
    agemax_unit = forms.ChoiceField(label=_('Maximum Age Unit'), 
                                   choices=choices.INCLUSION_AGE_UNIT)
    # TRDS 14e
    exclusion_criteria = forms.CharField(required=False, label=_('Exclusion Criteria'),
                                        max_length=8000)

    
    

