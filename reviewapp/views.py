# coding: utf-8
from django.http import Http404, HttpResponse
from reviewapp.models import UserProfile, REMARK_TRANSITIONS, Remark
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
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
from django.contrib.flatpages.models import FlatPage
from flatpages_polyglot.models import FlatPageTranslation
from tickets.models import Ticket

from reviewapp.models import Submission, News
from reviewapp.forms import UploadTrial, InitialTrialForm, OpenRemarkForm
from reviewapp.forms import UserForm, PrimarySponsorForm, UserProfileForm
from reviewapp.forms import ContactForm, ConsentForm
from reviewapp.consts import REMARK, MISSING, PARTIAL, COMPLETE

from repository.models import ClinicalTrial, CountryCode, ClinicalTrialTranslation
from repository.trds_forms import TRIAL_FORMS
from repository.trial_validation import trial_validator
from datetime import datetime
import pickle
from utilities import safe_truncate

def index(request):
        
    show_beta_message = request.session.get('show_beta_message', True)

    # if the HTTP_REFERER is empty or the HTTP_HOST is not the same as HTTP_REFERER, 
    # strength display the message
    referer = request.META.get('HTTP_REFERER', '')
    http_host = request.META.get('HTTP_HOST', '')
    if not referer or referer.find(http_host) == -1:
        show_beta_message = True
        
    if show_beta_message:
        request.session['show_beta_message'] = False

    clinical_trials = ClinicalTrial.published.all()[:3]
    
    pages = FlatPage.objects.filter(url='/site-description/')
    if len(pages) < 1:
        trans = None
    else:
        page = pages[0]
        try:
            trans = page.translations.get(language__iexact=request.LANGUAGE_CODE)
        except FlatPageTranslation.DoesNotExist:
            trans = page
            
    beta_pages = FlatPage.objects.filter(url='/beta-message/')
    if len(beta_pages) < 1:
        beta_trans = None
    else:
        beta_page = beta_pages[0]
        try:
            beta_trans = beta_page.translations.get(language__iexact=request.LANGUAGE_CODE)
        except FlatPageTranslation.DoesNotExist:
            beta_trans = beta_page

    if not beta_trans:
        show_beta_message = False

    return render_to_response('reviewapp/index.html', {
                          'clinical_trials': clinical_trials,
                          'page': trans,
                          'beta_page': beta_trans,
                          'show_beta_message': show_beta_message},
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
    
    # Gets the list of submissions
    submission = Submission.objects.filter(creator=request.user)

    # Submission list is optimized to retunrs only the necessary fields
    submission_list = submission.values('pk','created','title','status',
            'trial__pk','trial__scientific_title')
            
    for sub in submission_list:
        sub['can_delete'] = submission.get(pk=sub['pk']).can_delete()

    def objects_with_title_translated():
        # TODO for #125: Change this to a better solution
        for obj in submission_list:
            obj['title'] = obj['trial__scientific_title']
            try:
                #t = obj.trial.translations.get(language=request.LANGUAGE_CODE)
                t = ClinicalTrialTranslation.objects.get_translation_for_object(
                        request.LANGUAGE_CODE, model=ClinicalTrial, object_id=obj['trial__pk'],
                        )
                if t.scientific_title != '':
                    obj['title'] = t.scientific_title
            except ObjectDoesNotExist:
                pass

            # Forces a safe trancate
            obj['short_title'] = safe_truncate(obj['title'], 120)

            yield obj
    
    object_list = objects_with_title_translated()
    
    delete = False
    no_delete = False
    if request.GET.get('delete'):
        if request.GET.get('delete') == 'ok':
            delete = True
        elif request.GET.get('delete') == 'no':
            no_delete = True
    
    return render_to_response('reviewapp/submission_list.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def submission_detail(request,pk):
    object = get_object_or_404(Submission, id=int(pk))
    return render_to_response('reviewapp/submission_detail.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def submission_delete(request, id):
    submission = get_object_or_404(Submission, pk=id)
    if not request.user.is_staff:
        if request.user != submission.creator:
            return render_to_response('403.html', {'site': Site.objects.get_current(),},
                            context_instance=RequestContext(request))
    if submission.can_delete():
        if hasattr(submission, 'trial'):
            submission.trial.delete()
        submission.delete()
        return HttpResponseRedirect('/accounts/submissionlist/?delete=ok')
    else:
        return HttpResponseRedirect('/accounts/submissionlist/?delete=no')

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
            
            next = request.GET.get('next', '')
            if next:
                response = HttpResponseRedirect(next)
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
        consent_form = ConsentForm(request.POST, display_language=request.user.get_profile().preferred_language)
        if consent_form.is_valid():
            initial_form = InitialTrialForm(user=request.user)
            sponsor_form = PrimarySponsorForm()

            forms = [initial_form, sponsor_form]
            return render_to_response('reviewapp/new_submission.html', {
                'forms': forms },
                context_instance=RequestContext(request))
        else:
            initial_form = InitialTrialForm(request.POST,request.FILES)
            sponsor_form = PrimarySponsorForm(request.POST)

            if initial_form.is_valid() and sponsor_form.is_valid():
                trial = ClinicalTrial()
                su = Submission(creator=request.user)
                su.language = initial_form.cleaned_data['language']
                su.title = initial_form.cleaned_data['scientific_title']
                if su.language == 'en':
                    trial.scientific_title = su.title
                else:
                    trial.save()
                    ctt = ClinicalTrialTranslation()
                    ctt.language = su.language
                    ctt.scientific_title = su.title
                    trial.translations.add(ctt)

                trial.save()
                su.save()
                
                sponsor = sponsor_form.save(commit=False)
                sponsor.creator = request.user
                sponsor.save()
                
                trial.primary_sponsor = su.primary_sponsor = sponsor
                trial.recruitment_country = [CountryCode.objects.get(pk=id) for id in initial_form.cleaned_data['recruitment_country']]
                su.trial = trial

                trial.save()
                su.save()
                
                # sets the initial status of the fields
                fields_status = {}
                FIELDS = {
                    TRIAL_FORMS[0]: MISSING, TRIAL_FORMS[1]: PARTIAL, TRIAL_FORMS[2]: MISSING,

                    TRIAL_FORMS[3]: MISSING, TRIAL_FORMS[4]: MISSING, TRIAL_FORMS[5]: MISSING, 
                    TRIAL_FORMS[6]: MISSING, TRIAL_FORMS[7]: MISSING, TRIAL_FORMS[8]: PARTIAL
                }
                for lang in su.get_mandatory_languages():
                    lang = lang.lower()
                    fields_status.update({lang: dict(FIELDS)})
                    if lang == su.language.lower():
                        fields_status[lang].update({TRIAL_FORMS[0]: PARTIAL})
                
                su.fields_status = pickle.dumps(fields_status)
                su.save()

                return HttpResponseRedirect(reverse('repository.edittrial',args=[trial.id]))    
    else:
        consent_form = ConsentForm(display_language=request.user.get_profile().preferred_language)

    form = consent_form
    return render_to_response('reviewapp/consent.html', {
        'form': form},
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

            # Executes validation of current trial submission (for mandatory fields)
            trial_validator.validate(submission.trial)
            
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
    
    # Executes validation of current trial submission (for mandatory fields)
    trial_validator.validate(remark.submission.trial)
    
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

