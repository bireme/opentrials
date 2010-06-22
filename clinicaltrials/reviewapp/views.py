# coding: utf-8
from django.http import Http404, HttpResponse
from reviewapp.models import UserProfile, REMARK_TRANSITIONS, Remark
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, Context
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from tickets.models import Ticket

from reviewapp.models import Submission, News
from reviewapp.forms import UploadTrial, InitialTrialForm, OpenRemarkForm
from reviewapp.forms import UserForm, PrimarySponsorForm, UserProfileForm
from reviewapp.forms import ContactForm

from repository.models import ClinicalTrial, CountryCode
from datetime import datetime

def index(request):
    clinical_trials = ClinicalTrial.published.all()[:3]
    latest = News.objects.filter(status__exact='published').order_by('-created',)[:1]
    if len(latest) < 1:
        latest = None
    else:
        latest = latest[0]
    return render_to_response('reviewapp/index.html', {
                              'clinical_trials': clinical_trials,
                              'news': latest,},
                              context_instance=RequestContext(request))

@login_required
def dashboard(request):
    user_submissions = Submission.objects.filter(creator=request.user)
    remarks = Remark.objects.filter(submission__in=user_submissions)
    
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
            
            if request.GET['next']:
                response = HttpResponseRedirect(request.GET['next'])
            else:
                response = HttpResponseRedirect(reverse('reviewapp.submissionlist'))

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
        
def resend_activation_email(request):
    
    email = request.GET.get('email', '')
    users = User.objects.filter(email=email)
    
    if len(users) > 0:
        user = users[0]
    else:
        return render_to_response('reviewapp/resend_activation_email.html', 
                {'user_exist': False, 'email': email},
                context_instance=RequestContext(request))
        
    if user.is_active:
        return HttpResponseRedirect(reverse('reviewapp.password_reset')+'?email='+email)
    else:
   
        profiles = RegistrationProfile.objects.filter(user=user)
        
        if len(profiles) > 0:
            profile = profiles[0]
            
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            
            user.date_joined = datetime.now()
            user.last_login = datetime.now()
            user.save()
            profile.send_activation_email(site)

            return render_to_response('reviewapp/resend_activation_email.html', 
                {'user_exist': True},
                context_instance=RequestContext(request))
        else:
            return render_to_response('reviewapp/resend_activation_email.html', 
                {'user_exist': False, 'email': email},
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

@permission_required('reviewapp.add_remark')
def open_remark(request, submission_id, context):
    submission = get_object_or_404(Submission, id=int(submission_id))

    if request.POST:
        form = OpenRemarkForm(request.POST)

        if form.is_valid():
            remark = form.save(commit=False)
            remark.creator = request.user
            remark.submission = submission
            remark.context = context
            remark.status = 'opened'
            form.save()

            return HttpResponseRedirect(reverse('repository.trialview',args=[submission.trial.id]))

    form = OpenRemarkForm()
    return render_to_response('reviewapp/open_remark.html', locals(),
        context_instance=RequestContext(request))

@login_required
def change_remark_status(request, remark_id, status):

    if status not in REMARK_TRANSITIONS:
        raise Http404

    remark = get_object_or_404(Remark, id=int(remark_id))
    if status not in REMARK_TRANSITIONS[remark.status]:
        return HttpResponse(status=403)

    remark.status = status
    remark.save()
    return HttpResponse(remark.status, mimetype='text/plain')
    
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = request.POST.get('subject', '')
            message = request.POST.get('message', '')
            name = request.POST.get('name', '')
            from_email = '%s <%s>' % (name,
                                      request.POST.get('from_email', ''))
            recipient_list = [mail_tuple[1] for mail_tuple in settings.ADMINS]
            try:
                t = loader.get_template('reviewapp/email_contact.txt')
                c = Context({
                            'name': name,
                            'message': message,
                            'site': Site.objects.get_current() })
                send_mail(subject, t.render(c), from_email, recipient_list,
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/?sent=ok')
    else:
        form = ContactForm()
    sent = bool(request.GET.get('sent', ''))
    return render_to_response('reviewapp/contact.html', {
                              'form': form, 
                              'sent': sent },
                              context_instance=RequestContext(request))

