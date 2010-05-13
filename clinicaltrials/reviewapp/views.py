# coding: utf-8
from reviewapp.models import UserProfile
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from tickets.models import Ticket

from reviewapp.models import Submission
from reviewapp.trds_forms import UploadTrial, InitialTrialForm
from reviewapp.trds_forms import UserForm, PrimarySponsorForm, UserProfileForm

from repository.models import ClinicalTrial, CountryCode

def index(request):
    return render_to_response('reviewapp/index.html', locals())

@login_required
def dashboard(request):
    user_tickets = Ticket.objects.filter(creator=request.user)[:5]
    user_submissions = Submission.objects.filter(creator=request.user)[:5]
    return render_to_response('reviewapp/dashboard.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('reviewapp/user_dump.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def submissions_list(request):
    object_list = Submission.objects.filter(creator=request.user)
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_list.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def submission_detail(request,pk):
    object = get_object_or_404(Submission, id=int(pk))
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('reviewapp/submission_detail.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,instance=profile)                     
        password_form = PasswordChangeForm(request.user,request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            response = HttpResponseRedirect(reverse('reviewapp.dashboard'))
            if hasattr(request, 'session'):
                request.session['django_language'] = profile.preferred_language
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, profile.preferred_language)

            if password_form.changed_data:
                if password_form.is_valid():
                    password_form.save()
                    return response
            else:
                return response
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render_to_response('reviewapp/user_profile.html', locals(),
        context_instance=RequestContext(request))

@login_required
def new_submission(request):
    if request.method == 'POST':
        initial_form = InitialTrialForm(request.POST,request.FILES)
        sponsor_form = PrimarySponsorForm(request.POST)

        if initial_form.is_valid() and sponsor_form.is_valid():
            trial = ClinicalTrial()
            su = Submission(creator=request.user)
            su.language = initial_form.cleaned_data['language']
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
        'forms': forms },
        context_instance=RequestContext(request))

@login_required
def upload_trial(request):
    return render_to_response('reviewapp/upload_trial.html', {
        'form': UploadTrial()},
        context_instance=RequestContext(request))