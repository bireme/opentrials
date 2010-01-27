#coding: utf-8


from clinicaltrials.registry.models import ClinicalTrial
from clinicaltrials.registry.models import TrialInterventionCode
from clinicaltrials.registry.models import SpecificDescriptor
from clinicaltrials.registry.models import GeneralDescriptor
from clinicaltrials.registry.models import TrialSupportSource
from clinicaltrials.registry.models import TrialSecondarySponsor

from clinicaltrials.vocabulary.models import InterventionCode

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django import forms

from clinicaltrials.registry.trds_forms import PrimarySponsorForm, HealthConditionsForm
from choices import INSTITUTIONAL_RELATION, DESCRIPTOR_LEVEL

EXTRA_SECONDARY_IDS = 2

#
# Forms 
#

class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['primary_sponsor',]

    title = _('Primary Sponsor')

class SecondarySponsorForm(forms.ModelForm):
    class Meta:
        model = TrialSecondarySponsor
        fields = ['institution','relation']

    relation = forms.CharField(widget=forms.HiddenInput, initial=INSTITUTIONAL_RELATION[1][0])

class SupportSourceForm(forms.ModelForm):
    class Meta:
        model = TrialSupportSource
        fields = ['institution','relation']
    relation = forms.CharField(widget=forms.HiddenInput, initial=INSTITUTIONAL_RELATION[0][0])

class GeneralDescriptorForm(forms.ModelForm):
    class Meta:
        model = GeneralDescriptor
        fields = ['descriptor']
    level = forms.CharField(widget=forms.HiddenInput, initial=DESCRIPTOR_LEVEL[0][0])

class SpecificDescriptorForm(forms.ModelForm):
    class Meta:
        model = SpecificDescriptor
        fields = ['descriptor']
    level = forms.CharField(widget=forms.HiddenInput, initial=DESCRIPTOR_LEVEL[1][0])

class InterventionForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['i_freetext','i_code']
    title = _('Intervention(s)')
    
    i_freetext = forms.CharField(label=_('Intervention(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

    i_code = forms.ModelMultipleChoiceField(label=_("Intervention Code(s)"),
                                            queryset=InterventionCode.objects.all(),
                                            widget=forms.CheckboxSelectMultiple())

##

def step_2(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = PrimarySponsorForm(request.POST, instance=ct)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
                           form=SecondarySponsorForm,extra=EXTRA_SECONDARY_IDS)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
                           form=SupportSourceForm,extra=EXTRA_SECONDARY_IDS)

        secondary_forms = SecondarySponsorSet(request.POST, instance=ct)
        sources_form = SupportSourceSet(request.POST, instance=ct)

        if form.is_valid() and secondary_forms.is_valid() and sources_form.is_valid():
            form.save()
            secondary_forms.save()
            sources_form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_3/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = PrimarySponsorForm(instance=ct)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
            form=SecondarySponsorForm,extra=EXTRA_SECONDARY_IDS, can_delete=True)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
               form=SupportSourceForm,extra=EXTRA_SECONDARY_IDS,can_delete=True)
        
        secondary_forms = SecondarySponsorSet(instance=ct)
        sources_form = SupportSourceSet(instance=ct)

    forms = {'main':form, 'secondary':secondary_forms, 'sources':sources_form}
    return render_to_response('registry/trial_form_step_2.html',
                              {'forms':forms,
                               'next_form_title':_('Health Conditions Form')})

def step_3(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = HealthConditionsForm(request.POST, instance=ct)
        GeneralDescriptorSet = inlineformset_factory(ClinicalTrial, GeneralDescriptor,
                           form=GeneralDescriptorForm,extra=EXTRA_SECONDARY_IDS)
        SpecificDescriptorSet = inlineformset_factory(ClinicalTrial, SpecificDescriptor,
                           form=SpecificDescriptorForm,extra=EXTRA_SECONDARY_IDS)

        general_forms = GeneralDescriptorSet(request.POST, instance=ct)
        specific_forms = SpecificDescriptorSet(request.POST, instance=ct)

        if form.is_valid() and general_forms.is_valid() and specific_forms.is_valid():
            form.save()
            general_forms.save()
            specific_forms.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_3/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = HealthConditionsForm(instance=ct)
        GeneralDescriptorSet = inlineformset_factory(ClinicalTrial, GeneralDescriptor,
            form=GeneralDescriptorForm,extra=EXTRA_SECONDARY_IDS, can_delete=True)
        SpecificDescriptorSet = inlineformset_factory(ClinicalTrial, SpecificDescriptor,
               form=SpecificDescriptorForm,extra=EXTRA_SECONDARY_IDS,can_delete=True)

        general_forms = GeneralDescriptorSet(instance=ct)
        specific_forms = SpecificDescriptorSet(instance=ct)

    forms = {'main':form, 'general':general_forms, 'specific':specific_forms}
    return render_to_response('registry/trial_form_step_3.html',
                              {'forms':forms,
                               'next_form_title':_('Interventions Form')})

def step_4(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = InterventionForm(request.POST, instance=ct)

        if form.is_valid():
            form.save(commit=False)
            ct.i_code.clear()
            ct.save()

            for code in request.POST.getlist('i_code'):
                icode = InterventionCode(int(code))
                TrialInterventionCode.objects.create(trial=ct,i_code=icode)                

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_5/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = InterventionForm(instance=ct)

    forms = {'main':form}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Health Conditions Form')})