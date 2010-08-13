# coding: utf-8

from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.db.models import Q
from django.views.generic.list_detail import object_list
from django.conf import settings
from django.template.defaultfilters import slugify
from django.template.context import RequestContext

from reviewapp.models import Attachment, Submission, Remark, SUBMISSION_STATUS
from reviewapp.forms import ExistingAttachmentForm,NewAttachmentForm
from reviewapp.consts import STEP_STATES, REMARK, MISSING, PARTIAL, COMPLETE

from repository.trial_validation import trial_validator
from repository.models import ClinicalTrial, Descriptor, TrialNumber
from repository.models import TrialSecondarySponsor, TrialSupportSource, Outcome
from repository.models import PublicContact, ScientificContact, SiteContact, Contact, Institution
from repository.trds_forms import MultilingualBaseFormSet
from repository.trds_forms import GeneralHealthDescriptorForm, PrimarySponsorForm
from repository.trds_forms import SecondaryIdForm, make_secondary_sponsor_form
from repository.trds_forms import make_support_source_form, TrialIdentificationForm
from repository.trds_forms import SpecificHealthDescriptorForm, HealthConditionsForm
from repository.trds_forms import InterventionDescriptorForm, InterventionForm
from repository.trds_forms import RecruitmentForm, StudyTypeForm, PrimaryOutcomesForm
from repository.trds_forms import SecondaryOutcomesForm, make_public_contact_form
from repository.trds_forms import make_scientifc_contact_form, make_contact_form, NewInstitution
from repository.trds_forms import make_site_contact_form, TRIAL_FORMS

from polyglot.multilingual_forms import modelformset_factory

import choices
import settings

import pickle

EXTRA_FORMS = 1

MENU_SHORT_TITLE = [_('Trial Identif.'),
                    _('Spons.'),
                    _('Health Cond.'),
                    _('Interv.'),
                    _('Recruit.'),
                    _('Study Type'),
                    _('Outcomes'),
                    _('Contacts'),
                    _('Attachs')]

@login_required
def edit_trial_index(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    status = ct.submission.get_status()
    
    if status in [REMARK, MISSING]:
        submit = False
    else:
        submit = True

    if request.POST and submit:
        sub = ct.submission
        sub.status = SUBMISSION_STATUS[1][0]

        sub.save()
        return HttpResponseRedirect(reverse('reviewapp.dashboard'))
    else:
        ''' start view '''
        
        fields_status = ct.submission.get_fields_status()

        links = []
        for i, name in enumerate(TRIAL_FORMS):
            data = dict(label=_(name))
            data['url'] = reverse('step_' + str(i + 1), args=[trial_pk])
            
            trans_list = []
            for lang in ct.submission.get_mandatory_languages():
                trans = {}
                lang = lang.lower()
                step_status = fields_status.get(lang, {}).get(name, None)
                if step_status == MISSING:
                    trans['icon'] = settings.MEDIA_URL + 'images/form-status-missing.png'
                elif step_status == PARTIAL: 
                    trans['icon'] = settings.MEDIA_URL + 'images/form-status-partial.png'
                elif step_status == COMPLETE:
                    trans['icon'] = settings.MEDIA_URL + 'images/form-status-complete.png'
                elif step_status == REMARK:
                    trans['icon'] = settings.MEDIA_URL + 'images/form-status-remark.png'
                else:
                    trans['icon'] = settings.MEDIA_URL + 'media/img/admin/icon_error.gif'
                
                if step_status is None:
                    trans['msg'] = _('Error')
                else:
                    trans['msg'] = _(STEP_STATES[(step_status-1)][1].title())
                trans_list.append(trans)
            data['trans'] = trans_list
            links.append(data)
        
        status_message = {}
        if status == REMARK:
            status_message['icon'] = settings.MEDIA_URL + 'images/form-status-remark.png'
            status_message['msg'] = _("There are fields with remarks.")
        elif status == MISSING:
            status_message['icon'] = settings.MEDIA_URL + 'images/form-status-missing.png'
            status_message['msg'] = _("There are required fields missing.")
        elif status == PARTIAL:
            status_message['icon'] = settings.MEDIA_URL + 'images/form-status-partial.png'
            status_message['msg'] = _("All required fields were filled.")
        elif status == COMPLETE:
            status_message['icon'] = settings.MEDIA_URL + 'images/form-status-complete.png'
            status_message['msg'] = _("All fields were filled.")
        else:
            status_message['icon'] = settings.MEDIA_URL + 'media/img/admin/icon_error.gif'
            status_message['msg'] = _("Error")
        
        return render_to_response('repository/trial_index.html',
                                  {'trial_pk':trial_pk,
                                   'submission':ct.submission,
                                   'links':links,
                                   'status': status,
                                   'submit': submit,
                                   'status_message': status_message,},
                                   context_instance=RequestContext(request))

def full_view(request, trial_pk):
    ''' full view '''
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    return render_to_response('repository/trds.html',
                              {'fieldtable':ct.html_dump()},
                               context_instance=RequestContext(request))


@login_required
def list_all(request, page=0, **kwargs):
    ''' List all trials of a user logged
        If you use a search term, the result is filtered 
    '''
    q = request.GET.get('q', '')
    queryset = ClinicalTrial.objects.filter(submission__creator=request.user)
    if q:
        queryset = queryset.filter(Q(scientific_title__icontains=q)
                                               |Q(public_title__icontains=q)
                                               |Q(trial_id__iexact=q)
                                               |Q(acronym__iexact=q)
                                               |Q(acronym_expansion__icontains=q)
                                               |Q(scientific_acronym__iexact=q)
                                               |Q(scientific_acronym_expansion__icontains=q))

    return object_list(
                  request,
                  queryset = queryset,
                  paginate_by = getattr(settings, 'PAGINATOR_CT_PER_PAGE', 10),
                  page = page,
                  extra_context = {'q': q,},
                  **kwargs)


def index(request, page=0, **kwargs):
    ''' List all registered trials
        If you use a search term, the result is filtered 
    '''
    q = request.GET.get('q', '')
    if q:
        queryset = ClinicalTrial.published.filter(Q(scientific_title__icontains=q)
                                               |Q(public_title__icontains=q)
                                               |Q(trial_id__iexact=q)
                                               |Q(acronym__iexact=q)
                                               |Q(acronym_expansion__icontains=q)
                                               |Q(scientific_acronym__iexact=q)
                                               |Q(scientific_acronym_expansion__icontains=q))
    else:
        queryset = ClinicalTrial.published.all()

    return object_list(
                  request,
                  queryset = queryset,
                  paginate_by = getattr(settings, 'PAGINATOR_CT_PER_PAGE', 10),
                  page = page,
                  extra_context = {'q': q,},
                  **kwargs)

@login_required
def trial_view(request, trial_pk):
    ''' show details of a trial of a user logged '''
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk), submission__creator=request.user)
    translations = [t for t in ct.translations.all()]
    return render_to_response('repository/clinicaltrial_detail_user.html',
                                {'object': ct,
                                'translations': translations,
                                'host': request.get_host()},
                                context_instance=RequestContext(request))
                                
def trial_registered(request, trial_id):
    ''' show details of a trial registered '''
    ct = get_object_or_404(ClinicalTrial, trial_id=trial_id, status='published')
    translations = [t for t in ct.translations.all()]
    return render_to_response('repository/clinicaltrial_detail.html',
                                {'object': ct,
                                'translations': translations,
                                'host': request.get_host()},
                                context_instance=RequestContext(request))

@login_required
def new_institution(request):

    if request.POST:
        new_institution = NewInstitution(request.POST)
        if new_institution.is_valid():
            institution = new_institution.save(commit=False)
            institution.creator = request.user
            institution.save()
            json = serializers.serialize('json',[institution])
            return HttpResponse(json, mimetype='application/json')
        else:
            return HttpResponse(new_institution.as_table(), mimetype='text/html')

    else:
        new_institution = NewInstitution()

    return render_to_response('repository/new_institution.html',
                             {'form':new_institution},
                               context_instance=RequestContext(request))

def step_list(trial_pk):
    import sys
    current_step = int( sys._getframe(1).f_code.co_name.replace('step_','') )
    steps = []
    for i in range(1,10):
        steps.append({'link': reverse('step_%d'%i,args=[trial_pk]), 
                      'is_current': (i == current_step), 
                      'name': MENU_SHORT_TITLE[i-1]})
    return steps

@login_required
def step_1(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = TrialIdentificationForm(request.POST, instance=ct,
                                       display_language=request.user.get_profile().preferred_language)
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber,
                                               form=SecondaryIdForm,
                                               extra=EXTRA_FORMS)
        secondary_forms = SecondaryIdSet(request.POST, instance=ct)

        if form.is_valid() and secondary_forms.is_valid():
            secondary_forms.save()
            form.save()
            return HttpResponseRedirect(reverse('step_1',args=[trial_pk]))
    else:
        form = TrialIdentificationForm(instance=ct, 
                                       default_second_language=ct.submission.get_secondary_language(),
                                       display_language=request.user.get_profile().preferred_language,
                                       )
        SecondaryIdSet = inlineformset_factory(ClinicalTrial, TrialNumber,
                                               form=SecondaryIdForm,
                                               extra=EXTRA_FORMS, can_delete=True)
        secondary_forms = SecondaryIdSet(instance=ct)

    forms = [form]
    formsets = [secondary_forms]
    return render_to_response('repository/trial_form.html',
                              {'forms':forms,'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[0],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[0])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],
                               },
                               context_instance=RequestContext(request))


@login_required
def step_2(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    
    qs_primary_sponsor = Institution.objects.filter(creator=request.user).order_by('name')

    if request.POST:
        form = PrimarySponsorForm(request.POST, instance=ct, queryset=qs_primary_sponsor,
                                  display_language=request.user.get_profile().preferred_language)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
                           form=make_secondary_sponsor_form(request.user),extra=EXTRA_FORMS)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
                           form=make_support_source_form(request.user),extra=EXTRA_FORMS)

        secondary_forms = SecondarySponsorSet(request.POST, instance=ct)
        sources_form = SupportSourceSet(request.POST, instance=ct)

        if form.is_valid() and secondary_forms.is_valid() and sources_form.is_valid():
            secondary_forms.save()
            sources_form.save()
            form.save()
        return HttpResponseRedirect(reverse('step_2',args=[trial_pk]))
    else:
        form = PrimarySponsorForm(instance=ct, queryset=qs_primary_sponsor,
                                  default_second_language=ct.submission.get_secondary_language(),
                                  display_language=request.user.get_profile().preferred_language)
        SecondarySponsorSet = inlineformset_factory(ClinicalTrial, TrialSecondarySponsor,
            form=make_secondary_sponsor_form(request.user),extra=EXTRA_FORMS, can_delete=True)
        SupportSourceSet = inlineformset_factory(ClinicalTrial, TrialSupportSource,
               form=make_support_source_form(request.user),extra=EXTRA_FORMS,can_delete=True)

        secondary_forms = SecondarySponsorSet(instance=ct)
        sources_form = SupportSourceSet(instance=ct)

    forms = [form]
    formsets = [secondary_forms,sources_form]
    return render_to_response('repository/step_2.html',
                              {'forms':forms,'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[1],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[1])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_3(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    GeneralDescriptorSet = modelformset_factory(Descriptor,
                                                formset=MultilingualBaseFormSet,
                                                form=GeneralHealthDescriptorForm,
                                                can_delete=True,
                                                extra=EXTRA_FORMS,
                                                extra_formset_attrs={
                                                    'default_second_language':ct.submission.get_secondary_language(),
                                                    'available_languages':[lang.lower() for lang in ct.submission.get_mandatory_languages()],
                                                    'display_language':request.user.get_profile().preferred_language,
                                                    },
                                                )

    SpecificDescriptorSet = modelformset_factory(Descriptor,
                                                formset=MultilingualBaseFormSet,
                                                form=SpecificHealthDescriptorForm,
                                                can_delete=True,
                                                extra=EXTRA_FORMS,
                                                extra_formset_attrs={
                                                    'default_second_language':ct.submission.get_secondary_language(),
                                                    'available_languages':[lang.lower() for lang in ct.submission.get_mandatory_languages()],
                                                    'display_language':request.user.get_profile().preferred_language,
                                                    },
                                                )

    general_qs = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[0][0],
                                           level=choices.DESCRIPTOR_LEVEL[0][0])

    specific_qs = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[0][0],
                                           level=choices.DESCRIPTOR_LEVEL[1][0])

    if request.POST:
        form = HealthConditionsForm(request.POST, instance=ct,
                                    display_language=request.user.get_profile().preferred_language)
        general_desc_formset = GeneralDescriptorSet(request.POST,queryset=general_qs,prefix='g')
        specific_desc_formset = SpecificDescriptorSet(request.POST,queryset=specific_qs,prefix='s')

        if form.is_valid() and general_desc_formset.is_valid() and specific_desc_formset.is_valid():
            descriptors = general_desc_formset.save(commit=False)
            descriptors += specific_desc_formset.save(commit=False)
            

            for descriptor in descriptors:
                descriptor.trial = ct

            general_desc_formset.save()
            specific_desc_formset.save()
            form.save()
            
            return HttpResponseRedirect(reverse('step_3',args=[trial_pk]))
    else:
        form = HealthConditionsForm(instance=ct,
                                    default_second_language=ct.submission.get_secondary_language(),
                                    display_language=request.user.get_profile().preferred_language)
        general_desc_formset = GeneralDescriptorSet(queryset=general_qs,prefix='g')
        specific_desc_formset = SpecificDescriptorSet(queryset=specific_qs,prefix='s')


    forms = [form]
    formsets = [general_desc_formset, specific_desc_formset]
    return render_to_response('repository/step_3.html',
                              {'forms':forms,'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[2],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[2])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_4(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    DescriptorFormSet = modelformset_factory(Descriptor,
                                          formset=MultilingualBaseFormSet,
                                          form=InterventionDescriptorForm,
                                          can_delete=True,
                                          extra=EXTRA_FORMS,
                                          extra_formset_attrs={
                                            'default_second_language':ct.submission.get_secondary_language(),
                                            'available_languages':[lang.lower() for lang in ct.submission.get_mandatory_languages()],
                                            'display_language':request.user.get_profile().preferred_language,
                                            },
                                          )

    queryset = Descriptor.objects.filter(trial=trial_pk,
                                           aspect=choices.TRIAL_ASPECT[1][0],
                                           level=choices.DESCRIPTOR_LEVEL[0][0])
    if request.POST:
        form = InterventionForm(request.POST, instance=ct,
                                display_language=request.user.get_profile().preferred_language)
        specific_desc_formset = DescriptorFormSet(request.POST, queryset=queryset)

        if form.is_valid() and specific_desc_formset.is_valid():
            descriptors = specific_desc_formset.save(commit=False)


            for descriptor in descriptors:
                descriptor.trial = ct

            specific_desc_formset.save()
            form.save()
            return HttpResponseRedirect(reverse('step_4',args=[trial_pk]))
    else:
        form = InterventionForm(instance=ct,
                                default_second_language=ct.submission.get_secondary_language(),
                                display_language=request.user.get_profile().preferred_language)
        specific_desc_formset = DescriptorFormSet(queryset=queryset)

    forms = [form]
    formsets = [specific_desc_formset]
    return render_to_response('repository/step_4.html',
                              {'forms':forms,'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[3],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[3])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_5(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = RecruitmentForm(request.POST, instance=ct,
                               display_language=request.user.get_profile().preferred_language)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('step_5',args=[trial_pk]))
    else:
        form = RecruitmentForm(instance=ct,
                               default_second_language=ct.submission.get_secondary_language(),
                               display_language=request.user.get_profile().preferred_language)

    forms = [form]
    return render_to_response('repository/trial_form.html',
                              {'forms':forms,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[4],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[4])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_6(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    if request.POST:
        form = StudyTypeForm(request.POST, instance=ct,
                             display_language=request.user.get_profile().preferred_language)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('step_6',args=[trial_pk]))
    else:
        form = StudyTypeForm(instance=ct, 
                             default_second_language=ct.submission.get_secondary_language(),
                             display_language=request.user.get_profile().preferred_language)

    forms = [form]
    return render_to_response('repository/trial_form.html',
                              {'forms':forms,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[5],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[5])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_7(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    PrimaryOutcomesSet = modelformset_factory( Outcome,
                                formset=MultilingualBaseFormSet,
                                form=PrimaryOutcomesForm,extra=EXTRA_FORMS,
                                can_delete=True,
                                extra_formset_attrs={
                                    'default_second_language':ct.submission.get_secondary_language(),
                                    'available_languages':[lang.lower() for lang in ct.submission.get_mandatory_languages()],
                                    'display_language':request.user.get_profile().preferred_language,
                                    },
                                )
    SecondaryOutcomesSet = modelformset_factory(Outcome,
                                formset=MultilingualBaseFormSet,
                                form=SecondaryOutcomesForm,extra=EXTRA_FORMS,
                                can_delete=True,
                                extra_formset_attrs={
                                    'default_second_language':ct.submission.get_secondary_language(),
                                    'available_languages':[lang.lower() for lang in ct.submission.get_mandatory_languages()],
                                    'display_language':request.user.get_profile().preferred_language,
                                    },
                                )

    primary_qs = Outcome.objects.filter(trial=ct, interest=choices.OUTCOME_INTEREST[0][0])
    secondary_qs = Outcome.objects.filter(trial=ct, interest=choices.OUTCOME_INTEREST[1][0])

    if request.POST:
        primary_outcomes_formset = PrimaryOutcomesSet(request.POST, queryset=primary_qs, prefix='primary')
        secondary_outcomes_formset = SecondaryOutcomesSet(request.POST, queryset=secondary_qs, prefix='secondary')

        if primary_outcomes_formset.is_valid() and secondary_outcomes_formset.is_valid():
            outcomes = primary_outcomes_formset.save(commit=False)
            outcomes += secondary_outcomes_formset.save(commit=False)

            for outcome in outcomes:
                outcome.trial = ct

            primary_outcomes_formset.save()
            secondary_outcomes_formset.save()

            # Executes validation of current trial submission (for mandatory fields)
            trial_validator.validate(ct)

            return HttpResponseRedirect(reverse('step_7',args=[trial_pk]))
    else:
        primary_outcomes_formset = PrimaryOutcomesSet(queryset=primary_qs, prefix='primary')
        secondary_outcomes_formset = SecondaryOutcomesSet(queryset=secondary_qs, prefix='secondary')

    formsets = [primary_outcomes_formset,secondary_outcomes_formset]
    return render_to_response('repository/trial_form.html',
                              {'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[6],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[6])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


@login_required
def step_8(request, trial_pk):
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))

    contact_type = {
        'PublicContact': (PublicContact,make_public_contact_form(request.user)),
        'ScientificContact': (ScientificContact,make_scientifc_contact_form(request.user)),
        'SiteContact': (SiteContact,make_site_contact_form(request.user))
    }

    InlineFormSetClasses = []
    for model,form in contact_type.values():
        InlineFormSetClasses.append(
            inlineformset_factory(ClinicalTrial,model,form=form,can_delete=True,extra=EXTRA_FORMS)
        )

    ContactFormSet = modelformset_factory(Contact, form=make_contact_form(request.user), extra=1)

    contact_qs = Contact.objects.none()

    if request.POST:
        inlineformsets = [fs(request.POST,instance=ct) for fs in InlineFormSetClasses]
        new_contact_formset = ContactFormSet(request.POST,queryset=contact_qs,prefix='new_contact')

        if not False in [fs.is_valid() for fs in inlineformsets] \
                and new_contact_formset.is_valid():

            for contactform in new_contact_formset.forms:
                if contactform.cleaned_data:
                    Relation = contact_type[contactform.cleaned_data.pop('relation')][0]
                    new_contact = contactform.save(commit=False)
                    new_contact.creator = request.user
                    new_contact.save()
                    Relation.objects.create(trial=ct,contact=new_contact)

            for fs in inlineformsets:
                fs.save()

            # Executes validation of current trial submission (for mandatory fields)
            trial_validator.validate(ct)

            return HttpResponseRedirect(reverse('step_8',args=[trial_pk]))
    else:
        inlineformsets = [fs(instance=ct) for fs in InlineFormSetClasses]
        new_contact_formset = ContactFormSet(queryset=contact_qs,prefix='new_contact')

    formsets = inlineformsets + [new_contact_formset]
    return render_to_response('repository/step_8.html',
                              {'formsets':formsets,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[7],
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[7])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))

@login_required
def step_9(request, trial_pk):
    # TODO: this function should be on another place
    ct = get_object_or_404(ClinicalTrial, id=int(trial_pk))
    su = Submission.objects.get(trial=ct)
                                             
    NewAttachmentFormSet = modelformset_factory(Attachment,
                                             extra=1,
                                             can_delete=False,
                                             form=NewAttachmentForm)

    existing_attachments = Attachment.objects.filter(submission=su)

    if request.method == 'POST':
        new_attachment_formset = NewAttachmentFormSet(request.POST,
                                                      request.FILES,
                                                      prefix='new')

        if new_attachment_formset.is_valid():
            new_attachments = new_attachment_formset.save(commit=False)

            for attachment in new_attachments:
                attachment.submission = su

            new_attachment_formset.save()
            return HttpResponseRedirect(reverse('step_9',args=[trial_pk]))
    else:
        new_attachment_formset = NewAttachmentFormSet(queryset=Attachment.objects.none(),
                                                      prefix='new')

    formsets = [new_attachment_formset]
    return render_to_response('repository/attachments.html',
                              {'formsets':formsets,
                               'existing_attachments':existing_attachments,
                               'trial_pk':trial_pk,
                               'title':TRIAL_FORMS[8],
                               'host': request.get_host(),
                               'steps': step_list(trial_pk),
                               'remarks':Remark.opened.filter(submission=ct.submission,context=slugify(TRIAL_FORMS[8])),
                               'default_second_language': ct.submission.get_secondary_language(),
                               'available_languages': [lang.lower() for lang in ct.submission.get_mandatory_languages()],},
                               context_instance=RequestContext(request))


