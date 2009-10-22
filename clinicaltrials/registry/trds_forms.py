# coding: utf-8

from django import forms
from django.utils.translation import ugettext as _

#from django.contrib.admin.widgets import AdminDateWidget

from models import Institution

import choices
from vocabulary.models import CountryCode, RecruitmentStatus
from vocabulary.models import StudyType, StudyPhase

from clinicaltrials.registry.models import ClinicalTrial, Institution
    

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
    # TRDS 9a
    public_title = forms.CharField(required=False, 
                                   label=_('Public Title'),
                                   max_length=2000, 
                                   widget=forms.Textarea)
    # TRDS 9b
    acronym = forms.CharField(required=False, label=_('Acronym'),
                              max_length=255)

    # TODO: Secondary Numbers

class SponsorsForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['primary_sponsor_name','primary_sponsor_address',
                 'primary_sponsor_country'] 

    title = _('Sponsors and Sources of Support')

    # TRDS 5
    primary_sponsor_name = forms.CharField(required=False, 
                                           label=_('Primary Sponsor'),
                                           max_length=255)
    primary_sponsor_address = forms.CharField(required=False, 
                                              label=_('Postal Address'),
                                              widget=forms.Textarea)
    primary_sponsor_country = forms.ModelChoiceField(label=_('Country'),
                                    queryset=CountryCode.objects.all())

    # TODO: TRDS 4: Sources of Support
    # TODO: TRDS 6: Secondary Sponsors

class HealthConditionsForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['hc_freetext',]

    title = _('Health Condition(s) or Problem(s) Studied')

    # TRDS 12a
    hc_freetext = forms.CharField(label=_('Health Condition(s) or Problem(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

class InterventionsForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['i_freetext',]

    title = _('Intervention(s)')

    # TRDS 13a
    i_freetext = forms.CharField(label=_('Intervention(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)
class StudyTypeForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['study_type', 'study_design', 'phase']

    title = _('Study Type')

    # TRDS 15a
    study_type = forms.ModelChoiceField(label=_('Study Type'),
                                        queryset=StudyType.objects.all())

    # TRDS 15b
    study_design = forms.CharField(label=_('Study Design'),
                                         required=False, max_length=1000,
                                         widget=forms.Textarea)
    # TRDS 15c
    phase = forms.ModelChoiceField(label=_('Study Phase'),
                                   queryset=StudyPhase.objects.all())



class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['recruitment_status', 'date_enrollment', 'target_sample_size', 
                  'phase', 'inclusion_criteria', 'gender', 
                  'agemin_value', 'agemin_unit',
                  'agemax_value', 'agemax_unit', 'exclusion_criteria',
                  ]

    title = _('Recruitment')

    # TODO: Countries of Recruitment

    # TRDS 18
    recruitment_status = forms.ModelChoiceField(label=_('Recruitment Status'),
                                                queryset=RecruitmentStatus.objects.all())

    # TRDS 16a,b (type_enrollment: anticipated or actual)
    date_enrollment = forms.CharField( # yyyy-mm or yyyy-mm-dd
        label=_('Date of First Enrollment'), max_length=10, required=False)

    # TRDS 17
    target_sample_size = forms.IntegerField(label=_('Target Sample Size'),
                                             initial=0 , required=False)
    # TRDS 14a
    inclusion_criteria = forms.CharField(label=_('Inclusion Criteria'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)
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
    exclusion_criteria = forms.CharField(label=_('Exclusion Criteria'),required=False,
                                        max_length=8000, widget=forms.Textarea,)

class ContactForm(forms.Form):
    title = _('Contacts')

    firstname = forms.CharField(label=_('First Name'), max_length=50)
    middlename = forms.CharField(label=_('Middle Name'), max_length=50)
    lastname = forms.CharField(label=_('Last Name'), max_length=50)

    email = forms.EmailField(label=_('E-mail'), max_length=255)

    affiliation = forms.ModelChoiceField(Institution.objects.all(),
                                         _('Affiliation'))

    address = forms.CharField(label=_('Address'), max_length=255)
    city = forms.CharField(label=_('City'), max_length=255)

    country = forms.ModelChoiceField(CountryCode.objects.all(), _('Country'))

    zip = forms.CharField(label=_('Postal Code'), max_length=50)
    telephone = forms.CharField(label=_('Telephone'), max_length=255)
