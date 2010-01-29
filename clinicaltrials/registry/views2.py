#coding: utf-8

from clinicaltrials.vocabulary.models import CountryCode
from clinicaltrials.registry.models import RecruitmentCountry
from clinicaltrials.registry.models import ClinicalTrial
from clinicaltrials.registry.models import Descriptor
from clinicaltrials.registry.models import GeneralDescriptor
from clinicaltrials.registry.models import Outcome
from clinicaltrials.registry.models import RecruitmentStatus
from clinicaltrials.registry.models import SpecificDescriptor
from clinicaltrials.registry.models import StudyType
from clinicaltrials.registry.models import StudyPhase
from clinicaltrials.registry.models import TrialInterventionCode
from clinicaltrials.registry.models import TrialSecondarySponsor
from clinicaltrials.registry.models import TrialSupportSource

from clinicaltrials.vocabulary.models import InterventionCode

import choices

from django import forms
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404

EXTRA_SECONDARY_IDS = 2

#
# Forms 
#

#step2
class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['primary_sponsor',]

    title = _('Primary Sponsor')

#step2
class SecondarySponsorForm(forms.ModelForm):
    class Meta:
        model = TrialSecondarySponsor
        fields = ['institution','relation']

    relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[1][0])

#step2
class SupportSourceForm(forms.ModelForm):
    class Meta:
        model = TrialSupportSource
        fields = ['institution','relation']
    relation = forms.CharField(widget=forms.HiddenInput, initial=choices.INSTITUTIONAL_RELATION[0][0])

#step3
class HealthConditionsForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['hc_freetext',]

    title = _('Health Condition(s) or Problem(s) Studied')

    # TRDS 12a
    hc_freetext = forms.CharField(label=_('Health Condition(s) or Problem(s)'),
                                         required=False, max_length=8000,
                                         widget=forms.Textarea)

#step3
class GeneralDescriptorForm(forms.ModelForm):
    class Meta:
        model = GeneralDescriptor
        fields = ['descriptor']
    level = forms.CharField(widget=forms.HiddenInput, initial=choices.DESCRIPTOR_LEVEL[0][0])

#step3
class SpecificDescriptorForm(forms.ModelForm):
    class Meta:
        model = SpecificDescriptor
        fields = ['descriptor']
    level = forms.CharField(widget=forms.HiddenInput, initial=choices.DESCRIPTOR_LEVEL[1][0])

#step4
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
#step5
class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['recruitment_status', 'recruitment_country','date_enrollment',
                  'target_sample_size', 'phase', 'inclusion_criteria', 'gender',
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

#step6
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

#step7
class OutcomesForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['interest','description']

    title = _('Outcomes')

#step8
class DescriptorForm(forms.ModelForm):
    class Meta:
        model = Descriptor

    title = _('Descriptor')
##ENDFORMS

#v-sponsors
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

#v-healthcondition
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
                return HttpResponseRedirect("/rg/step_4/%s/" % trial_pk)
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

#v-interventions
def step_4(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = InterventionForm(request.POST, instance=ct)

        if form.is_valid():
            form.save(commit=False)
            ct.i_code.clear()
            ct.save()

            for code in request.POST.getlist('i_code'):
                icode = InterventionCode(pk=int(code))
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
                               'next_form_title':_('Recruitment Form')})

#v-recruitment
def step_5(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = RecruitmentForm(request.POST, instance=ct)

        if form.is_valid():
            form.save(commit=False)
            ct.recruitment_country.clear()
            ct.save()

            for code in request.POST.getlist('recruitment_country'):
                ccode = CountryCode(pk=int(code))
                RecruitmentCountry.objects.create(trial=ct,country=ccode)

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_6/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = RecruitmentForm(instance=ct)

    forms = {'main':form}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Study Type Form')})

#v-studytype
def step_6(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = StudyTypeForm(request.POST, instance=ct)

        if form.is_valid():
            form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_7/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = StudyTypeForm(instance=ct)

    forms = {'main':form}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Outcomes Form')})

#v-outcomes
def step_7(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    OutcomesSet = inlineformset_factory(ClinicalTrial, Outcome,
                                form=OutcomesForm,extra=EXTRA_SECONDARY_IDS)

    if request.POST:
        formset = OutcomesSet(request.POST, instance=ct)

        if formset.is_valid():
            formset.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_7/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        formset = OutcomesSet(instance=ct)

    forms = {'main':formset}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Descriptor Form')})

#v-descriptor
def step_8(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    
#    DescriptorSet = inlineformset_factory(ClinicalTrial, Descriptor,
#                                form=DescriptorForm,extra=EXTRA_SECONDARY_IDS)

    if request.POST:
        formset = DescriptorForm(request.POST, instance=ct)

        if formset.is_valid():
            formset.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_7/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        formset = DescriptorForm(instance=ct)

    forms = {'main':formset}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms})


