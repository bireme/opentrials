# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext as _

from rebrac.models import Submission
from registry.models import ClinicalTrial, Institution
from vocabulary.models import CountryCode

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('rebrac/index.html', locals())

def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('rebrac/user_dump.html', locals())

####################################################### New Submission form ###

class InitialTrialForm(forms.Form):
    title = _('Initial Data fields')
    scientific_title = forms.CharField(label=_('Scientific Title'),
                                       max_length=2000,
                                       widget=forms.Textarea)
    recruitment_countries = forms.MultipleChoiceField(label=_('Countries of Recruitment'),
                                                      choices=CountryCode.choices())

class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    title = _('Primary Sponsor')

'''
class RecruitmentCountry(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    country = models.ForeignKey(CountryCode, verbose_name=_('Country'))

'''

def new_submission(request):
    if request.method == 'POST': # If the forms were submitted...
        initial_form = InitialTrialForm(request.POST)
        sponsor_form = PrimarySponsorForm(request.POST)
        if initial_form.is_valid() and sponsor_form.is_valid(): # All validation rules pass
            trial = ClinicalTrial(scientific_title=initial_form.cleaned_data['scientific_title'])
            trial.primary_sponsor = Institution.objects.create(**sponsor_form.cleaned_data)
            trial.save()
            for country_id in initial_form.cleaned_data['recruitment_countries']:
                trial.recruitmentcountry_set.create(country_id=country_id)
            submission = Submission(creator=request.user, trial=trial)
            submission.save()
            return HttpResponseRedirect(reverse('edittrial',args=[trial.id]))

    else:
        initial_form = InitialTrialForm()
        sponsor_form = PrimarySponsorForm()

    return render_to_response('rebrac/new_submission.html', {
        'initial_form': initial_form,
        'sponsor_form': sponsor_form,
    })
