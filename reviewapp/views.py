# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from django.forms.models import modelformset_factory
from reviewapp.models import Submission, Attachment
from registry.models import ClinicalTrial, CountryCode, Institution

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/index.html', locals())

def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('reviewapp/user_dump.html', locals())

def submissions_list(request):
    object_list = Submission.objects.all()
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_list.html', locals())

def submission_detail(request,pk):
    object = get_object_or_404(Submission, id=int(pk))
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_detail.html', locals())

####################################################### New Submission form ###

class InitialTrialForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['scientific_title','recruitment_country']

    title = _('Initial Trial Data')
    recruitment_country = forms.ModelMultipleChoiceField(
                                            label=_('Recruitment Country'),
                                            queryset=CountryCode.objects.all())

class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    title = _('Primary Sponsor')

@login_required
def new_submission(request):

    AttachmentForm = modelformset_factory(Attachment, extra=1, can_delete=False,
                                          exclude='submission')
    AttachmentForm.title = _('Attachments')

    if request.method == 'POST':
        initial_form = InitialTrialForm(request.POST)
        sponsor_form = PrimarySponsorForm(request.POST)
        attachment_formset = AttachmentForm(request.POST,request.FILES,
                                            queryset=Attachment.objects.none())

        if initial_form.is_valid() and sponsor_form.is_valid() and attachment_formset.is_valid():
            initial_form.instance.primary_sponsor = sponsor_form.save()
            trial = initial_form.save()


            submission = Submission(creator=request.user,
                                    trial=trial,
                                    primary_sponsor=trial.primary_sponsor,
                                    title=trial.scientific_title)
            submission.save()

            for af in attachment_formset.forms:
                af.instance.submission = submission;
            
            attachment_formset.save();
            return HttpResponseRedirect(reverse('registry.edittrial',args=[trial.id]))
    else:
        initial_form = InitialTrialForm()
        sponsor_form = PrimarySponsorForm()
        attachment_formset = AttachmentForm(queryset=Attachment.objects.none())


    forms = [initial_form, sponsor_form]
    return render_to_response('reviewapp/new_submission.html', {
        'forms': forms,
        'formset': attachment_formset,
        'username':request.user.username,
    })
