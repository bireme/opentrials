# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AnonymousUser

from reviewapp.models import Submission
from registry.models import ClinicalTrial, Institution
from vocabulary.models import CountryCode

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/index.html', locals())

def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('reviewapp/user_dump.html', locals())

####################################################### New Submission form ###

class InitialTrialForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial
        fields = ['scientific_title','recruitment_country']

    title = _('Initial Data fields')

class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    title = _('Primary Sponsor')

def new_submission(request):
    if request.user.__class__ is AnonymousUser:
        return HttpResponseRedirect(reverse('reviewapp.login'))

    if request.method == 'POST': # If the forms were submitted...
        initial_form = InitialTrialForm(request.POST)
        sponsor_form = PrimarySponsorForm(request.POST)

        if initial_form.is_valid() and sponsor_form.is_valid():
            initial_form.instance.primary_sponsor = sponsor_form.save()
            trial = initial_form.save()
            submission = Submission(creator=request.user, trial=trial)
            submission.save()
            return HttpResponseRedirect(reverse('edittrial',args=[trial.id]))
    else:
        initial_form = InitialTrialForm()
        sponsor_form = PrimarySponsorForm()

    return render_to_response('reviewapp/new_submission.html', {
        'initial_form': initial_form,
        'sponsor_form': sponsor_form,
    })
