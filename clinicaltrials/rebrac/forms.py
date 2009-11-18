from django import forms
from django.utils.translation import ugettext as _

from clinicaltrials.registry.models import ClinicalTrial, Institution


class SubmissionForm(forms.Form):
    class Meta:
        fields = ['scientific_title','primary_sponsor']

    title = _('Submission')
    
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000,
                                       widget=forms.Textarea)

    primary_sponsor = forms.ModelChoiceField(label=_('Primary Sponsor'),
                                             queryset=Institution.objects.all())

