#coding: utf-8

from clinicaltrials.registry.models import ScientificContact
from clinicaltrials.registry.models import PublicContact
from clinicaltrials.vocabulary.models import CountryCode

from clinicaltrials.registry.models import ClinicalTrial
from clinicaltrials.registry.models import Contact
from clinicaltrials.registry.models import Descriptor
from clinicaltrials.registry.models import Institution

from clinicaltrials.registry.models import Outcome
from clinicaltrials.registry.models import RecruitmentStatus

from clinicaltrials.registry.models import StudyType
from clinicaltrials.registry.models import StudyPhase

from clinicaltrials.registry.models import TrialSecondarySponsor
from clinicaltrials.registry.models import TrialSupportSource

from clinicaltrials.vocabulary.models import InterventionCode

import choices

from django import forms
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory, modelformset_factory, formset_factory
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404

EXTRA_FORMS = 2

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
class DescriptorForm(forms.ModelForm):
    class Meta:
        model = Descriptor
    trial = forms.CharField(widget=forms.HiddenInput,required=False)

    def clean(self):
        
        return super(forms.ModelForm,self).clean()

class GeneralHealthDescriptorForm(DescriptorForm):
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.DESCRIPTOR_LEVEL[0][0])

class SpecificHealthDescriptorForm(DescriptorForm):
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[0][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[1][0])

#step4
class InterventionDescriptorForm(DescriptorForm):
    aspect = forms.CharField(widget=forms.HiddenInput,
                              initial=choices.TRIAL_ASPECT[1][0])
    level = forms.CharField(widget=forms.HiddenInput,
                             initial=choices.DESCRIPTOR_LEVEL[0][0])

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
        fields = ['study_design', 'phase']

    title = _('Study Type')

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
class PublicContactForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['contact']

    relation = forms.CharField(initial=choices.CONTACT_RELATION[0][0],
                               widget=forms.HiddenInput)

#step8
class ScientificContactForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['contact']

    relation = forms.CharField(initial=choices.CONTACT_RELATION[1][0],
                               widget=forms.HiddenInput)

#step8-partof
class ContactForm(forms.Form):

    relation = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=choices.CONTACT_RELATION)

    firstname = forms.CharField(label=_('First Name'), max_length=50)
    middlename = forms.CharField(label=_('Middle Name'), max_length=50,required=False)
    lastname = forms.CharField(label=_('Last Name'), max_length=50)

    email = forms.EmailField(label=_('E-mail'), max_length=255)

    affiliation = forms.ModelChoiceField(Institution.objects.all(),
                                         _('Affiliation'))

    address = forms.CharField(label=_('Address'), max_length=255,required=False)
    city = forms.CharField(label=_('City'), max_length=255)

    country = forms.ModelChoiceField(CountryCode.objects.all(), _('Country'))

    zip = forms.CharField(label=_('Postal Code'), max_length=50)
    telephone = forms.CharField(label=_('Telephone'), max_length=255)




##ENDFORMS

#v-sponsors
def step_2(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = PrimarySponsorForm(request.POST, instance=ct)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
                           form=SecondarySponsorForm,extra=EXTRA_FORMS)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
                           form=SupportSourceForm,extra=EXTRA_FORMS)

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
            form=SecondarySponsorForm,extra=EXTRA_FORMS, can_delete=True)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
               form=SupportSourceForm,extra=EXTRA_FORMS,can_delete=True)

        secondary_forms = SecondarySponsorSet(instance=ct)
        sources_form = SupportSourceSet(instance=ct)

    forms = {'main':form, 'secondary':secondary_forms, 'sources':sources_form}
    return render_to_response('registry/trial_form_step_2.html',
                              {'forms':forms,
                               'next_form_title':_('Health Conditions Form')})

#v-healthcondition
def step_3(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    GeneralDescriptorSet = modelformset_factory(Descriptor,
                                                form=GeneralHealthDescriptorForm,
                                                extra=EXTRA_FORMS)

    SpecificDescriptorSet = modelformset_factory(Descriptor,
                                                form=SpecificHealthDescriptorForm,
                                                extra=EXTRA_FORMS)

    general_qs = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[0][0],
                                           level=choices.DESCRIPTOR_LEVEL[0][0])
                                           
    specific_qs = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[0][0],
                                           level=choices.DESCRIPTOR_LEVEL[1][0])


    if request.POST:
        form = HealthConditionsForm(request.POST, instance=ct)
        gdesc = GeneralDescriptorSet(request.POST,queryset=general_qs,prefix='g')
        sdesc = SpecificDescriptorSet(request.POST,queryset=specific_qs,prefix='s')

        if form.is_valid() and gdesc.is_valid() and sdesc.is_valid():

            for cdata in gdesc.cleaned_data+sdesc.cleaned_data:
                cdata['trial'] = ct

            form.save()
            gdesc.save()
            sdesc.save()            

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_4/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = HealthConditionsForm(instance=ct)
        gdesc = GeneralDescriptorSet(queryset=general_qs,prefix='g')
        sdesc = SpecificDescriptorSet(queryset=specific_qs,prefix='s')
        

    forms = {'main':form, 'general':gdesc, 'specific': sdesc}
    return render_to_response('registry/trial_form_step_3.html',
                              {'forms':forms,
                               'next_form_title':_('Interventions Form')})

#v-interventions
def step_4(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    DescriptorFormSet = modelformset_factory(Descriptor,
                                          form=InterventionDescriptorForm,
                                          extra=EXTRA_FORMS)
                                          
    queryset = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[1][0],
                                           level=choices.DESCRIPTOR_LEVEL[0][0])
    if request.POST:
        form = InterventionForm(request.POST, instance=ct)
        idesc = DescriptorFormSet(request.POST, queryset=queryset)

        if form.is_valid() and idesc.is_valid():

            for cdata in idesc.cleaned_data:
                cdata['trial'] = ct

            idesc.save()
            form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_5/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = InterventionForm(instance=ct)
        idesc = DescriptorFormSet(queryset=queryset)

    forms = {'main':form,'descriptor':idesc}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Recruitment Form')})

#v-recruitment
def step_5(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = RecruitmentForm(request.POST, instance=ct)

        if form.is_valid():
            form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_6/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        form = RecruitmentForm(instance=ct)

    forms = {'main':form}
    return render_to_response('registry/trial_form_step_5.html',
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
    return render_to_response('registry/trial_form_step_6.html',
                              {'forms':forms,
                               'next_form_title':_('Outcomes Form')})

#v-outcomes
def step_7(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    OutcomesSet = inlineformset_factory(ClinicalTrial, Outcome,
                                form=OutcomesForm,extra=EXTRA_FORMS)

    if request.POST:
        formset = OutcomesSet(request.POST, instance=ct)

        if formset.is_valid():
            formset.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_8/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        formset = OutcomesSet(instance=ct)

    forms = {'main':formset}
    return render_to_response('registry/trial_form_step_4.html',
                              {'forms':forms,
                               'next_form_title':_('Descriptor Form')})

#v-contact
def step_8(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    contact_type = {'PublicContact':PublicContact,
                    'ScientificContact':ScientificContact}

    PublicContactFormSet = inlineformset_factory(ClinicalTrial,
                                                contact_type['PublicContact'],
                                                form=PublicContactForm,
                                                can_delete=False,
                                                extra=EXTRA_FORMS)
    ScientificContactFormSet = inlineformset_factory(ClinicalTrial,
                                                contact_type['ScientificContact'],
                                                form=ScientificContactForm,
                                                can_delete=False,
                                                extra=EXTRA_FORMS)

    ContactFormSet = formset_factory(ContactForm,extra=1)


    if request.POST:
        public_form_set = PublicContactFormSet(request.POST,
                                               instance=ct)
        scientific_form_set = ScientificContactFormSet(request.POST,
                                                       instance=ct)

        new_contact_formset = ContactFormSet(request.POST)

        if public_form_set.is_valid() \
                and scientific_form_set.is_valid() \
                and new_contact_formset.is_valid():

            for contact_data in new_contact_formset.cleaned_data:
                if contact_data:
                    Relation = contact_type[contact_data.pop('relation')]
                    new_contact = Contact.objects.create(**contact_data)
                    Relation.objects.create(trial=ct,contact=new_contact)

            public_form_set.save()
            scientific_form_set.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect("/rg/step_9/%s/" % trial_pk)
            # FIXME: use dynamic url
            return HttpResponseRedirect("/rg/edit/%s/" % trial_pk)
    else:
        public_form_set = PublicContactFormSet(instance=ct)
        scientific_form_set = ScientificContactFormSet(instance=ct)
        new_contact_formset = ContactFormSet()

    forms = {'public':public_form_set,
             'scientific':scientific_form_set,
             'new': new_contact_formset }
    return render_to_response('registry/trial_form_step_8.html',
                              {'forms':forms})
