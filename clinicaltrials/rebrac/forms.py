from django import forms
from django.utils.translation import ugettext as _

from clinicaltrials.registry.models import ClinicalTrial


class SubmissionForm(forms.Form):
    class Meta:
        fields = ['scientific_title','scientific_acronym','public_title','acronym']

    title = _('Submission')
    
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000,
                                       widget=forms.Textarea)
    # TRDS 10b
    scientific_acronym = forms.CharField(required=True,
                                         label=_('Scientific Acronym'),
                                         max_length=255)
    # TRDS 9a
    public_title = forms.CharField(required=True,
                                   label=_('Public Title'),
                                   max_length=2000,
                                   widget=forms.Textarea)
    # TRDS 9b
    acronym = forms.CharField(required=True, label=_('Acronym'),
                              max_length=255)
