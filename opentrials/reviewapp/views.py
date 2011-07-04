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
from django.contrib import messages
from django.utils.translation import ugettext as _

from flatpages_polyglot.models import FlatPageTranslation
from tickets.models import Ticket
from utilities import user_in_group

from reviewapp.models import Submission, STATUS_PENDING, STATUS_RESUBMIT, STATUS_DRAFT
from reviewapp.models import SUBMISSION_TRANSITIONS, STATUS_APPROVED
from reviewapp.models import News, NewsTranslation
from reviewapp.forms import UploadTrialForm, InitialTrialForm, OpenRemarkForm
from reviewapp.forms import UserForm, PrimarySponsorForm, UserProfileForm
from reviewapp.forms import ContactForm, TermsUseForm, ResendActivationEmail
from reviewapp.forms import ImportParsedForm, ImportParsedFormset
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

    clinical_trials = fossil_trials.proxies(language=request.trials_language)

    return render_to_response('reviewapp/index.html', {
                          'clinical_trials': clinical_trials,
                          'page': flat_trans,},
                          context_instance=RequestContext(request))

@login_required
def dashboard(request):
    user_submissions = Submission.objects.filter(creator=request.user).order_by('-updated')
    remarks = Remark.objects.filter(submission__in=user_submissions)

    if request.user.has_perm('reviewapp.review'):
        submissions_to_review = Submission.objects.filter(status=STATUS_PENDING).order_by('-updated')

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
    submission_list = submission.values('pk','created','creator','title','status',
            'trial__pk','trial__scientific_title')

    for sub in submission_list:
        sub['can_delete'] = submission.get(pk=sub['pk']).can_delete()

    def objects_with_title_translated():
        # TODO for #125: Change this to a better solution
        for obj in submission_list:
            if obj['trial__scientific_title']:
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
        messages.success(request, _('The submission was deleted successfully.'))
    else:
        messages.warning(request, _('This submission can not be deleted.'))

    return HttpResponseRedirect('/accounts/submissionlist/')

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

    if request.method == 'POST':
        form = ResendActivationEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            if len(users) > 0:
                user = users[0]
            else:
                return render_to_response('reviewapp/resend_activation_email_complete.html',
                        {'user_exist': False, 'email': email},
                        context_instance=RequestContext(request))

            profiles = RegistrationProfile.objects.filter(user=user)
            if len(profiles) > 0:
                profile = profiles[0]

                if profile.activation_key == 'ALREADY_ACTIVATED':
                    return render_to_response('reviewapp/resend_activation_email_complete.html',
                        {'user_requestor': user},
                        context_instance=RequestContext(request))

                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)

                profile.send_activation_email(site)

                return render_to_response('reviewapp/resend_activation_email_complete.html',
                    {'user_exist': True, 'email': email},
                    context_instance=RequestContext(request))
            else:
                return render_to_response('reviewapp/resend_activation_email_complete.html',
                    {'user_exist': False, 'email': email},
                    context_instance=RequestContext(request))
    else:
        form = ResendActivationEmail()

    return render_to_response('reviewapp/resend_activation_email.html', {
                              'form': form, },
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
            if request.POST.get('submit') == _('Continue'):
                return HttpResponseRedirect(reverse('reviewapp.new_submission'))
            else:
                return HttpResponseRedirect('../uploadtrial')
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
        
        if initial_form.is_valid(): 
            trial = ClinicalTrial()

            su = Submission(creator=request.user)
            su.language = initial_form.cleaned_data['language']            
            su.title = initial_form.cleaned_data['scientific_title']            
            su.primary_sponsor = initial_form.cleaned_data['primary_sponsor']
            
            trial.utrn_number = initial_form.cleaned_data['utrn_number']
            trial.language = settings.DEFAULT_SUBMISSION_LANGUAGE
            trial.primary_sponsor = su.primary_sponsor

            if su.language == settings.DEFAULT_SUBMISSION_LANGUAGE:
                trial.scientific_title = su.title                                                            
            else:
                trial.save()
                ctt = ClinicalTrialTranslation.objects.get_translation_for_object(
                        su.language, trial, create_if_not_exist=True
                        )
                ctt.scientific_title = su.title
                ctt.save()
                
            trial.save()

            for country in initial_form.cleaned_data['recruitment_country']:
                trial.recruitment_country.add(country) # What about the removed ones? FIXME
            su.trial = trial

            trial.save()
            su.save()

            # sets the initial status of the fields
            su.init_fields_status()

            return HttpResponseRedirect(reverse('repository.edittrial',args=[trial.id]))
    else:
        initial_form = InitialTrialForm(user=request.user, display_language=request.trials_language)
        
    forms = [initial_form] 
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
    session_key = None
    form = None
    formset = None
    
    if request.method == 'POST':

        if 'submission_file' in request.FILES:
            form = UploadTrialForm(request.POST, files=request.FILES)
            if form.is_valid():
                parsed_trials = form.parse_file(request.user)

                session_key = 'parsed-trials-'+datetime.now().strftime('%Y%m%d%H%M%S')
                request.session[session_key] = [item for item in parsed_trials]

                formset = ImportParsedFormset(initial=[{
                    'trial_id': item[0]['trial_id'],
                    'description': item[0]['public_title'],
                    'already_exists': bool(item[1]),
                    'to_import': not item[1],
                    } for item in parsed_trials])


        elif 'session_key' in request.POST:
            
            formset = ImportParsedFormset(request.POST)
            if formset.is_valid():
                marked_trials = [form.cleaned_data['trial_id'] for form in formset.forms
                        if form.cleaned_data['to_import']]

                parsed_trials = request.session[request.POST['session_key']]
                parsed_trials = [t for t in parsed_trials if t[0]['trial_id'] in marked_trials]

                imported_trials = formset.import_file(parsed_trials, request.user)

                messages.info(request, _('XML files imported with success!'))

                # Slear parsed trials from session
                request.session.pop(request.POST['session_key'])

                return HttpResponseRedirect(reverse('reviewapp.uploadtrial'))
            
            else:
                form = UploadTrialForm()
    else:
        form = UploadTrialForm()
    
    if form is None:
        form = UploadTrialForm(request.POST, files=request.FILES)
    return render_to_response(
            'reviewapp/upload_trial.html',
            {'form': form, 'session_key': session_key, 'formset': formset},
            context_instance=RequestContext(request),
            )

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
                            'site_domain': Site.objects.get_current().domain,
                            'site_name': Site.objects.get_current().name, })
                send_mail(subject, t.render(c), from_email, recipient_list,
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, _('Message sent successfully.'))
            return HttpResponseRedirect('/contact/')
        else:
            messages.warning(request, _('Please fill out all fields correctly.'))
    else:
        if request.user.is_authenticated():
            form = ContactForm(user=request.user)
        else:
            form = ContactForm()

    return render_to_response('reviewapp/contact.html', {
                              'form': form, },
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
