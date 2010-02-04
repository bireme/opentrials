# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from reviewapp.models import Submission
from registry.models import ClinicalTrial, CountryCode, Institution

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
    if request.method == 'POST':
        initial_form = InitialTrialForm(request.POST)
        sponsor_form = PrimarySponsorForm(request.POST)

        if initial_form.is_valid() and sponsor_form.is_valid():
            initial_form.instance.primary_sponsor = sponsor_form.save()
            trial = initial_form.save()
            submission = Submission(creator=request.user, trial=trial,
                                                   title=trial.scientific_title)
            submission.save()
            return HttpResponseRedirect(reverse('edittrial',args=[trial.id]))
    else:
        initial_form = InitialTrialForm()
        sponsor_form = PrimarySponsorForm()

    return render_to_response('reviewapp/new_submission.html', {
        'initial_form': initial_form,
        'sponsor_form': sponsor_form,
    })
