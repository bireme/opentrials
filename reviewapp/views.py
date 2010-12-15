# coding: utf-8
from django.http import Http404, HttpResponse
from reviewapp.models import UserProfile, REMARK_TRANSITIONS, Remark
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
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
from django.utils.translation import get_language

from flatpages_polyglot.models import FlatPageTranslation
from tickets.models import Ticket
from utilities import user_in_group

from reviewapp.models import Submission, STATUS_PENDING, STATUS_RESUBMIT, STATUS_DRAFT
from reviewapp.models import SUBMISSION_TRANSITIONS, STATUS_APPROVED
from reviewapp.models import News, NewsTranslation
from reviewapp.forms import UploadTrial, InitialTrialForm, OpenRemarkForm
from reviewapp.forms import UserForm, PrimarySponsorForm, UserProfileForm
from reviewapp.forms import ContactForm, TermsUseForm
from reviewapp.consts import REMARK, MISSING, PARTIAL, COMPLETE

from repository.models import ClinicalTrial, CountryCode, ClinicalTrialTranslation
from repository.trds_forms import TRIAL_FORMS
from repository.trial_validation import trial_validator
from repository.choices import PROCESSING_STATUS
from datetime import datetime
from utilities import safe_truncate
from fossil.models import Fossil

def index(request):
        
    pages = FlatPage.objects.filter(url='/site-description/')
    if len(pages) < 1:
        flat_trans = None
    else:
        page = pages[0]
        try:
            flat_trans = page.translations.get(language__iexact=request.LANGUAGE_CODE)
        except FlatPageTranslation.DoesNotExist:
            flat_trans = page
        
    fossil_trials = ClinicalTrial.fossils.published().order_by('-creation')[:3]
    
    trials_language = 'en' # English is default if there's no choosen language
    if request.user.is_authenticated():
        trials_language = get_language()
    elif request.session.get('django_language', None):
        trials_language = request.session['django_language']
    elif request.COOKIES.get('django_language', None):
        trials_language = request.COOKIES['django_language']

    clinical_trials = fossil_trials.proxies(language=trials_language)

    return render_to_response('reviewapp/index.html', {
                          'clinical_trials': clinical_trials,
                          'page': flat_trans,},
                          context_instance=RequestContext(request))

@login_required
def dashboard(request):
    user_submissions = Submission.objects.filter(creator=request.user)
    remarks = Remark.objects.filter(submission__in=user_submissions)

    if request.user.has_perm('reviewapp.review'):
        submissions_to_review = Submission.objects.filter(status=STATUS_PENDING)
    
    return render_to_response('reviewapp/dashboard.html', locals(),
                               context_instance=RequestContext(request))

@login_required
def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('reviewapp/user_dump.html', locals(),
                               context_instance=RequestContext(request))

@permission_required('reviewapp.review')
def reviewlist(request):
    submissions_to_review = Submission.objects.filter(status=STATUS_PENDING)
    return render_to_response(
            'reviewapp/review_list.html',
            locals(),
            context_instance=RequestContext(request),
            )

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
                        request.LANGUAGE_CODE.lower(), model=ClinicalTrial, object_id=obj['trial__pk'],
                        )
                if t.scientific_title != '':
                    obj['title'] = t.scientific_title
            except ObjectDoesNotExist:
                pass

            # Forces a safe truncate
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
def terms_of_use(request):

    pages = FlatPage.objects.filter(url='/terms-of-use/')
    if len(pages) < 1:
        flat_trans = None
    else:
        page = pages[0]
        try:
            flat_trans = page.translations.get(language__iexact=request.LANGUAGE_CODE)
        except FlatPageTranslation.DoesNotExist:
            flat_trans = page
            
    if request.method == 'POST':
        terms_form = TermsUseForm(request.POST)
        
        if terms_form.is_valid():
            return HttpResponseRedirect(reverse('reviewapp.new_submission'))
    else: 
        terms_form = TermsUseForm()
        
    form = terms_form
    return render_to_response('reviewapp/terms_of_use.html', {
                              'form': form, 
                              'page': flat_trans},
                              context_instance=RequestContext(request))
                              
@login_required
def new_submission(request):

    if request.method == 'POST':
        initial_form = InitialTrialForm(request.POST, request.FILES, user=request.user)
        #sponsor_form = PrimarySponsorForm(request.POST)

        if initial_form.is_valid(): # and sponsor_form.is_valid():
            trial = ClinicalTrial()

            su = Submission(creator=request.user)
            su.language = initial_form.cleaned_data['language']
            su.title = initial_form.cleaned_data['scientific_title']
            su.primary_sponsor = initial_form.cleaned_data['primary_sponsor']

            if su.language == 'en':
                trial.scientific_title = su.title
            else:
                trial.save()
                ctt = ClinicalTrialTranslation.objects.get_translation_for_object(
                        su.language, trial, create_if_not_exist=True
                        )
                ctt.scientific_title = su.title
                ctt.save()

            trial.primary_sponsor = su.primary_sponsor
            trial.language = su.language
            trial.save()

            su.save()

            #sponsor = sponsor_form.save(commit=False)
            #sponsor.creator = request.user
            #sponsor.save()
            
            #trial.primary_sponsor = su.primary_sponsor = sponsor
            for country in initial_form.cleaned_data['recruitment_country']:
                trial.recruitment_country.add(country) # What about the removed ones? FIXME
            #trial.recruitment_country = [CountryCode.objects.get(pk=id) for pk in initial_form.cleaned_data['recruitment_country']]
            su.trial = trial

            trial.save()
            su.save()
            
            # sets the initial status of the fields
            su.init_fields_status()

            return HttpResponseRedirect(reverse('repository.edittrial',args=[trial.id]))
    else: 
        initial_form = InitialTrialForm(user=request.user)
        #sponsor_form = PrimarySponsorForm() 
        
    forms = [initial_form] #, sponsor_form] 
    return render_to_response('reviewapp/new_submission.html', {
                              'forms': forms,},
                              context_instance=RequestContext(request))

@login_required
def submission_edit_published(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    submission.status = STATUS_DRAFT
    submission.save()

    trial = submission.trial
    trial.status = PROCESSING_STATUS
    trial.save()

    return HttpResponseRedirect(reverse('repository.edittrial', args=(submission.trial.pk,)))

@login_required
def upload_trial(request):
    return render_to_response('reviewapp/upload_trial.html', {
        'form': UploadTrial()},
        context_instance=RequestContext(request))

@permission_required('reviewapp.add_remark')
def open_remark(request, submission_id, context):
    submission = get_object_or_404(Submission, id=int(submission_id))

    if request.method == 'POST':
        form = OpenRemarkForm(request.POST)

        if form.is_valid():
            remark = form.save(commit=False)
            remark.creator = request.user
            remark.submission = submission
            remark.context = context
            remark.status = 'open'
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
    
    if request.is_ajax():
        return HttpResponse(remark.status, mimetype='text/plain')
    else:
        return HttpResponseRedirect(reverse('repository.views.trial_view', args=[remark.submission.trial.id]))
        
@login_required
def delete_remark(request, remark_id):

    remark = get_object_or_404(Remark, id=int(remark_id))
    if remark.status != 'open':
        return HttpResponse(status=403)

    trial = remark.submission.trial
    remark.delete()
    
    # Executes validation of current trial submission (for mandatory fields)
    trial_validator.validate(trial)
    
    return HttpResponseRedirect(reverse('repository.views.trial_view', args=[trial.id]))
    
@login_required
def change_submission_status(request, submission_pk, status):
    if status not in SUBMISSION_TRANSITIONS:
        raise Http404

    if not request.user.is_staff and not user_in_group(request.user, 'reviewers'):
        return render_to_response('403.html', {'site': Site.objects.get_current(),},
                        context_instance=RequestContext(request))
                        
    submission = get_object_or_404(Submission, id=int(submission_pk))
    
    if status not in SUBMISSION_TRANSITIONS[submission.status]:
        return HttpResponse(status=403)

    # not approve submissions with remarks
    if status == STATUS_APPROVED and submission.remark_set.exclude(status='closed').count() > 0:
        return HttpResponse(status=403)

    submission.status = status
    submission.save()
    
    return HttpResponseRedirect(reverse('repository.views.trial_view', args=[submission.trial.id]))
    
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
                              
def news_list(request):

    object_list = News.objects.filter(status__exact='published').order_by('-created',)
    
    for obj in object_list:
        try:
            trans = obj.translations.get(language__iexact=request.LANGUAGE_CODE)
        except NewsTranslation.DoesNotExist:
            trans = None
        
        if trans:
            if trans.title:
                obj.title = trans.title
            if trans.text:
                obj.text = trans.text
                
    # pagination
    paginator = Paginator(object_list, getattr(settings, 'PAGINATOR_CT_PER_PAGE', 10))
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        objects = paginator.page(page)
    except (EmptyPage, InvalidPage):
        objects = paginator.page(paginator.num_pages)
    
    return render_to_response('reviewapp/news_list.html', {
                              'objects': objects, 
                              'page': page,
                              'paginator': paginator, },
                               context_instance=RequestContext(request))

def news_detail(request, object_id):
    obj = get_object_or_404(News, id=int(object_id))
    
    try:
        trans = obj.translations.get(language__iexact=request.LANGUAGE_CODE)
    except NewsTranslation.DoesNotExist:
        trans = None
    
    if trans:
        if trans.title:
            obj.title = trans.title
        if trans.text:
            obj.text = trans.text
    
    return render_to_response('reviewapp/news_detail.html', {
                              'object': obj, },
                               context_instance=RequestContext(request))

