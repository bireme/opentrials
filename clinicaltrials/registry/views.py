#coding: utf-8

from registry.models import ClinicalTrial, Descriptor, TrialNumber
from registry.models import TrialSecondarySponsor, TrialSupportSource, Outcome
from registry.models import PublicContact, ScientificContact, Contact

from registry.trds_forms import GeneralHealthDescriptorForm, PrimarySponsorForm
from registry.trds_forms import SecondaryIdForm, SecondarySponsorForm
from registry.trds_forms import SupportSourceForm, TrialIdentificationForm
from registry.trds_forms import SpecificHealthDescriptorForm, HealthConditionsForm
from registry.trds_forms import InterventionDescriptorForm, InterventionForm
from registry.trds_forms import RecruitmentForm, StudyTypeForm, OutcomesForm
from registry.trds_forms import PublicContactForm, ScientificContactForm
from registry.trds_forms import ContactForm

import choices

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory, modelformset_factory

EXTRA_FORMS = 2
TRIAL_FORMS = ['TrialIdentificationForm', 'SponsorsForm',
               'HealthConditionsForm', 'InterventionsForm',
               'RecruitmentForm', 'StudyTypeForm','OutcomesForm',
               'DescriptorForm']

#v-edit
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

#v-index
def index(request):
    latest_clinicalTrials = ClinicalTrial.objects.all()[:5]
    t = loader.get_template('registry/latest_clinicalTrials.html')
    c  = Context({
        'latest_clinicalTrials': latest_clinicalTrials,
    })
    return HttpResponse(t.render(c))

#v-trial
def step_1(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    
    if request.POST:
        form = TrialIdentificationForm(request.POST, instance=ct)
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber,
                                               form=SecondaryIdForm,
                                               extra=EXTRA_FORMS)
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
                                               form=SecondaryIdForm,
                                               extra=EXTRA_FORMS, can_delete=True)
        secondary_forms = SecondaryIdSet(instance=ct)

    forms = {'main':form, 'secondary':secondary_forms}
    return render_to_response('registry/trial_form_step_1.html',
                              {'forms':forms,
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
                               'next_form_title':_('Sponsors and Sources of Support')})

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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)],
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

    ContactFormSet = modelformset_factory(Contact, form=ContactForm, extra=1)

    contact_qs = Contact.objects.none()

    if request.POST:
        public_form_set = PublicContactFormSet(request.POST,
                                               instance=ct)
        scientific_form_set = ScientificContactFormSet(request.POST,
                                                       instance=ct)

        new_contact_formset = ContactFormSet(request.POST,queryset=contact_qs)

        if public_form_set.is_valid() \
                and scientific_form_set.is_valid() \
                and new_contact_formset.is_valid():

            for contactform in new_contact_formset.forms:
                if contactform.cleaned_data:
                    Relation = contact_type[contactform.cleaned_data.pop('relation')]
                    new_contact = contactform.save()
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
        new_contact_formset = ContactFormSet(queryset=contact_qs)

    forms = {'public':public_form_set,
             'scientific':scientific_form_set,
             'new': new_contact_formset }
    return render_to_response('registry/trial_form_step_8.html',
                              {'forms':forms,
                               'links': ['/rg/step_%d/%s'%(i,trial_pk) for i in range(1,9)]})
