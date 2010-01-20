#coding: utf-8

from django import forms
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from clinicaltrials.registry.models import ClinicalTrial, TrialNumber

TRIAL_FORMS = ['TrialIdentificationForm', 'SponsorsForm', 
               'HealthConditionsForm', 'InterventionsForm',
               'RecruitmentForm', 'StudyTypeForm','OutcomesForm',
               'DescriptorForm',]

EXTRA_SECONDARY_IDS = 2

def edit_trial_index(request, trial_pk):
    ''' start view '''
    links = []
    for i, name in enumerate(TRIAL_FORMS):
        data = dict(label='form.title', form_name=name)
        data['step'] = 'step_' + str(i + 1)
        data['icon'] = '/media/img/admin/icon_alert.gif'
        data['msg'] = 'Blank fields'
        links.append(data)
    return render_to_response('registry/trial_index.html', 
                              {'trial_pk':trial_pk,'links':links})    

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


def step_1(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    
    if request.POST:
        form = TrialIdentificationForm(request.POST, instance=ct)
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber, 
                                                  extra=EXTRA_SECONDARY_IDS)
        secondary_forms = SecondaryIdSet(request.POST, instance=ct)

        if form.is_valid() and secondary_forms.is_valid():
            form.save()
            secondary_forms.save()

        if request.POST.has_key('submit_next'):
            return HttpResponseRedirect("/rg/step_2/%s/" % trial_pk)
        # FIXME: use dynamic url
        return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = TrialIdentificationForm(instance=ct)
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber, 
                                               extra=EXTRA_SECONDARY_IDS, can_delete=True)
        secondary_forms = SecondaryIdSet(instance=ct)

    forms = {'main':form, 'secondary':secondary_forms}    
    return render_to_response('registry/trial_form_step_1.html',
                              {'forms':forms,
                               'next_form_title':_('Sponsors and Sources of Support')})

