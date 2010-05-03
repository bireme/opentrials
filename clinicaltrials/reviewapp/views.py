# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from tickets.models import Ticket
from reviewapp.models import Submission
from repository.models import ClinicalTrial, CountryCode, Institution

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/index.html', locals())

@login_required
def dashboard(request):
    username = request.user.username
    user_tickets = Ticket.objects.order_by('-created').filter(creator=request.user)[:5]
    user_submissions = Submission.objects.order_by('-created').filter(creator=request.user)[:5]
    return render_to_response('reviewapp/dashboard.html', locals())

@login_required
def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('reviewapp/user_dump.html', locals())

@login_required
def submissions_list(request):
    object_list = Submission.objects.filter(creator=request.user)
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_list.html', locals())

@login_required
def submission_detail(request,pk):
    object = get_object_or_404(Submission, id=int(pk))
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_detail.html', locals())

####################################################### New Submission form ###

class InitialTrialForm(forms.Form):
    form_title = _('Initial Trial Data')
    scientific_title = forms.CharField(widget=forms.Textarea, label=_('Scientific Title'), max_length=2000)
    recruitment_country = forms.MultipleChoiceField(choices=((cc.pk,cc.description) for cc in CountryCode.objects.iterator()) )

class PrimarySponsorForm(forms.ModelForm):
    class Meta:
        model = Institution
        exclude = ['address']
    form_title = _('Primary Sponsor')

@login_required
def new_submission(request):
    if request.method == 'POST':
        initial_form = InitialTrialForm(request.POST,request.FILES)
        sponsor_form = PrimarySponsorForm(request.POST)

        if initial_form.is_valid() and sponsor_form.is_valid():
            trial = ClinicalTrial()
            su = Submission(creator=request.user)

            trial.scientific_title = su.title = initial_form.cleaned_data['scientific_title']

            trial.save()
            su.save()

            trial.primary_sponsor = su.primary_sponsor = sponsor_form.save()
            trial.recruitment_country = [CountryCode.objects.get(pk=id) for id in initial_form.cleaned_data['recruitment_country']]
            su.trial = trial

            trial.save()
            su.save()

            return HttpResponseRedirect(reverse('repository.edittrial',args=[trial.id]))
    else:
        initial_form = InitialTrialForm()
        sponsor_form = PrimarySponsorForm()


    forms = [initial_form, sponsor_form]
    return render_to_response('reviewapp/new_submission.html', {
        'forms': forms,
        'username':request.user.username,
    })
