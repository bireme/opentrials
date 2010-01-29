# coding: utf-8

from django import forms
from django.utils.translation import ugettext as _

#from django.contrib.admin.widgets import AdminDateWidget

from vocabulary.models import CountryCode

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
