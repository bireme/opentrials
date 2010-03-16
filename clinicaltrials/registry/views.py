#coding: utf-8

from reviewapp.models import Attachment, Submission
from reviewapp.trds_forms import ExistingAttachmentForm,NewAttachmentForm

from registry.models import ClinicalTrial, Descriptor, TrialNumber
from registry.models import TrialSecondarySponsor, TrialSupportSource, Outcome
from registry.models import PublicContact, ScientificContact, SiteContact, Contact

from registry.trds_forms import GeneralHealthDescriptorForm, PrimarySponsorForm
from registry.trds_forms import SecondaryIdForm, SecondarySponsorForm
from registry.trds_forms import SupportSourceForm, TrialIdentificationForm
from registry.trds_forms import SpecificHealthDescriptorForm, HealthConditionsForm
from registry.trds_forms import InterventionDescriptorForm, InterventionForm
from registry.trds_forms import RecruitmentForm, StudyTypeForm, OutcomesForm
from registry.trds_forms import PublicContactForm, ScientificContactForm
from registry.trds_forms import ContactForm, NewInstitution, SiteContactForm

import choices
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

EXTRA_FORMS = 1
TRIAL_FORMS = ['Trial Identification',
               'Sponsors',
               'Health Conditions',
               'Interventions',
               'Recruitment',
               'Study Type',
               'Outcomes',
               'Contacts',
               'Attachments']


@login_required
def edit_trial_index(request, trial_pk):
    ''' start view '''
    links = []
    for i, name in enumerate(TRIAL_FORMS):
        data = dict(label=_(name))
        data['url'] = reverse('step_' + str(i + 1), args=[trial_pk])
        data['icon'] = '/media/img/admin/icon_alert.gif'
        data['msg'] = 'Blank fields'
        links.append(data)
    return render_to_response('registry/trial_index.html',
                              {'username':request.user.username,
                               'trial_pk':trial_pk,
                               'links':links})

def full_view(request, trial_pk):
    ''' full view '''
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    return render_to_response('registry/trds.html',
                              {'fieldtable':ct.html_dump()})


@login_required
def index(request):
    latest_clinicalTrials = ClinicalTrial.objects.all()[:5]
    t = loader.get_template('registry/latest_clinicalTrials.html')
    c  = Context({
        'latest_clinicalTrials': latest_clinicalTrials,
    })
    return HttpResponse(t.render(c))

@login_required
def new_institution(request):

    if request.POST:
        new_institution = NewInstitution(request.POST)
        if new_institution.is_valid():
            institution = new_institution.save()
            json = serializers.serialize('json',[institution])
            return HttpResponse(json, mimetype='application/json');
    else:
        new_institution = NewInstitution()
    
    return render_to_response('registry/new_institution.html',
                             {'form':new_institution})

@login_required
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
                return HttpResponseRedirect(reverse("step_2",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = TrialIdentificationForm(instance=ct)
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber,
                                               form=SecondaryIdForm,
                                               extra=EXTRA_FORMS, can_delete=True)
        secondary_forms = SecondaryIdSet(instance=ct)

    forms = [form]
    formsets = [secondary_forms]
    return render_to_response('registry/trial_form.html',
                              {'forms':forms,'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[0],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Sponsors and Sources of Support')})


@login_required
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
                return HttpResponseRedirect(reverse("step_3",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = PrimarySponsorForm(instance=ct)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
            form=SecondarySponsorForm,extra=EXTRA_FORMS, can_delete=True)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
               form=SupportSourceForm,extra=EXTRA_FORMS,can_delete=True)

        secondary_forms = SecondarySponsorSet(instance=ct)
        sources_form = SupportSourceSet(instance=ct)

#    import pdb
#    pdb.set_trace()

    forms = [form]
    formsets = [secondary_forms,sources_form]
    return render_to_response('registry/step_2.html',
                              {'forms':forms,'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[1],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Health Conditions Form')})


@login_required
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
                return HttpResponseRedirect(reverse("step_4",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = HealthConditionsForm(instance=ct)
        gdesc = GeneralDescriptorSet(queryset=general_qs,prefix='g')
        sdesc = SpecificDescriptorSet(queryset=specific_qs,prefix='s')


    forms = [form]
    formsets = [gdesc, sdesc]
    return render_to_response('registry/step_3.html',
                              {'forms':forms,'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[2],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Interventions Form')})


@login_required
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
                return HttpResponseRedirect(reverse("step_5",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = InterventionForm(instance=ct)
        idesc = DescriptorFormSet(queryset=queryset)

    forms = [form]
    formsets = [idesc]
    return render_to_response('registry/trial_form.html',
                              {'forms':forms,'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[3],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Recruitment Form')})


@login_required
def step_5(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = RecruitmentForm(request.POST, instance=ct)

        if form.is_valid():
            form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect(reverse("step_6",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = RecruitmentForm(instance=ct)

    forms = [form]
    return render_to_response('registry/trial_form.html',
                              {'forms':forms,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[4],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Study Type Form')})


@login_required
def step_6(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = StudyTypeForm(request.POST, instance=ct)

        if form.is_valid():
            form.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect(reverse("step_7",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        form = StudyTypeForm(instance=ct)

    forms = [form]
    return render_to_response('registry/trial_form.html',
                              {'forms':forms,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[5],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Outcomes Form')})


@login_required
def step_7(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    OutcomesSet = inlineformset_factory(ClinicalTrial, Outcome,
                                form=OutcomesForm,extra=EXTRA_FORMS)

    if request.POST:
        outcomes_formset = OutcomesSet(request.POST, instance=ct)

        if outcomes_formset.is_valid():
            outcomes_formset.save()

            if request.POST.has_key('submit_next'):
                return HttpResponseRedirect(reverse("step_8",args=[trial_pk]))
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        outcomes_formset = OutcomesSet(instance=ct)

    formsets = [outcomes_formset]
    return render_to_response('registry/trial_form.html',
                              {'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[6],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)],
                               'next_form_title':_('Descriptor Form')})


@login_required
def step_8(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    contact_type = {'PublicContact':PublicContact,
                    'ScientificContact':ScientificContact,
                    'SiteContact':SiteContact}

    PublicContactFormSet = inlineformset_factory(ClinicalTrial,
                                                contact_type['PublicContact'],
                                                form=PublicContactForm,
                                                can_delete=True,
                                                extra=EXTRA_FORMS)
    ScientificContactFormSet = inlineformset_factory(ClinicalTrial,
                                                contact_type['ScientificContact'],
                                                form=ScientificContactForm,
                                                can_delete=True,
                                                extra=EXTRA_FORMS)
    SiteContactFormSet = inlineformset_factory(ClinicalTrial,
                                                contact_type['SiteContact'],
                                                form=SiteContactForm,
                                                can_delete=True,
                                                extra=EXTRA_FORMS)

    ContactFormSet = modelformset_factory(Contact, form=ContactForm, extra=1)

    contact_qs = Contact.objects.none()

    if request.POST:
        public_form_set = PublicContactFormSet(request.POST,
                                               instance=ct)
        scientific_form_set = ScientificContactFormSet(request.POST,
                                                       instance=ct)
        site_form_set = SiteContactFormSet(request.POST,
                                                    instance=ct)

        new_contact_formset = ContactFormSet(request.POST,queryset=contact_qs)

        if public_form_set.is_valid() \
                and scientific_form_set.is_valid() \
                and site_form_set.is_valid() \
                and new_contact_formset.is_valid():

            for contactform in new_contact_formset.forms:
                if contactform.cleaned_data:
                    Relation = contact_type[contactform.cleaned_data.pop('relation')]
                    new_contact = contactform.save()
                    Relation.objects.create(trial=ct,contact=new_contact)

            public_form_set.save()
            scientific_form_set.save()
            site_form_set.save()
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        public_form_set = PublicContactFormSet(instance=ct)
        scientific_form_set = ScientificContactFormSet(instance=ct)
        site_form_set = SiteContactFormSet(instance=ct)
        new_contact_formset = ContactFormSet(queryset=contact_qs)

    formsets = [public_form_set,scientific_form_set,site_form_set,new_contact_formset]
    return render_to_response('registry/trial_form.html',
                              {'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[7],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)]})

@login_required
def step_9(request, trial_pk):
    # TODO: this function should be on another place
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    su = Submission.objects.get(trial=ct)
    
    ExistingAttachmentFormSet = inlineformset_factory(Submission,
                                             Attachment,
                                             extra=0,
                                             can_delete=True,
                                             form=ExistingAttachmentForm)
    NewAttachmentFormSet = modelformset_factory(Attachment,
                                             extra=1,
                                             can_delete=False,
                                             form=NewAttachmentForm)


    if request.method == 'POST':

        existing_attachment_formset = ExistingAttachmentFormSet(request.POST,
                                                                request.FILES,
                                                                instance=su,
                                                                prefix='existing')
        new_attachment_formset = NewAttachmentFormSet(request.POST,
                                                      request.FILES,
                                                      prefix='new')

        if existing_attachment_formset.is_valid() and new_attachment_formset.is_valid():
            existing_attachment_formset.save()

            for cdata in new_attachment_formset.cleaned_data:
                cdata['submission'] = su

            new_attachment_formset.save()
            
            return HttpResponseRedirect(reverse("registry.edittrial", args=[trial_pk]))
    else:
        existing_attachment_formset = ExistingAttachmentFormSet(instance=su,
                                                                prefix='existing')
        new_attachment_formset = NewAttachmentFormSet(queryset=Attachment.objects.none(),
                                                      prefix='new')

    formsets = [existing_attachment_formset,new_attachment_formset]
    return render_to_response('registry/attachments.html',
                              {'formsets':formsets,
                               'username':request.user.username,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[8],
                               'links': [reverse('step_%d'%i,args=[trial_pk]) for i in range(1,10)]})
