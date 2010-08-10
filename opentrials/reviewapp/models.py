import pickle

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from repository.models import ClinicalTrial, Institution
from repository.choices import PROCESSING_STATUS, PUBLISHED_STATUS
from vocabulary.models import CountryCode
from utilities import safe_truncate

from tickets.models import Ticket

from django.db.models.signals import post_save

import settings


SUBMISSION_STATUS = [
    ('draft', 'draft'), # clinical trial is 'processing'
    ('pending', 'pending'), # clinical trial remains 'processing'
    ('approved', 'approved'), # clinical trial is 'published'
    ('rejected', 'rejected'), # clinical trial remains or becomes 'processing'
]
STATUS_DRAFT = SUBMISSION_STATUS[0][0]
STATUS_PENDING = SUBMISSION_STATUS[1][0]
STATUS_APPROVED = SUBMISSION_STATUS[2][0]
STATUS_REJECTED = SUBMISSION_STATUS[3][0]


ACCESS = [
    ('public', 'Public'),
    ('private', 'Private'),
]

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    preferred_language = models.CharField(_('Preferred language'),max_length=10,
                                choices=settings.MANAGED_LANGUAGES_CHOICES,
                                default=settings.MANAGED_LANGUAGES_CHOICES[-1][0])
                                
    def amount_submissions(self):
        return u"%03d" % (Submission.objects.filter(creator=self.user).count())

    def amount_tickets(self):
        return u"%03d" % (Ticket.objects.filter(creator=self.user).count())
       

class Submission(models.Model):
    class Meta:
        ordering = ['-created']
        permissions = (
            ("review", "Can review"),
        )

    creator = models.ForeignKey(User, related_name='submission_creator', editable=False)
    created = models.DateTimeField(default=datetime.now, editable=False)
    updater = models.ForeignKey(User, null=True, related_name='submission_updater', editable=False)
    updated = models.DateTimeField(null=True, editable=False)
    title = models.TextField(u'Scientific title', max_length=2000)
    primary_sponsor = models.OneToOneField(Institution, null=True, blank=True,
                                    verbose_name=_('Primary Sponsor'))

    trial = models.OneToOneField(ClinicalTrial, null=True)
    status = models.CharField(_('Status'), max_length=64,
                              choices=SUBMISSION_STATUS,
                              default=SUBMISSION_STATUS[0][0])
    fields_status = models.TextField(_('Fields Status'), max_length=512, null=True, 
                                     blank=True, editable=False)
    language = models.CharField(_('Submission language'), max_length=10,
                                choices=settings.MANAGED_LANGUAGES_CHOICES)
    staff_note = models.TextField(_('Submission note (staff use only)'), max_length=255,
                                    blank=True)

    def save(self):
        if self.id:
            self.updated = datetime.now()
        if self.status == STATUS_APPROVED and self.trial.status == PROCESSING_STATUS:
            self.trial.status = PUBLISHED_STATUS
            self.trial.save()
        if self.status == STATUS_REJECTED and self.trial.status == PUBLISHED_STATUS:
            self.trial.status = PROCESSING_STATUS
            self.trial.save()

        super(Submission, self).save()

    def short_title(self):
        return safe_truncate(self.title, 120)

    def creator_username(self):
        return self.creator.username

    def __unicode__(self):
        return self.short_title()

    def get_mandatory_languages(self):
        langs = set([u'en'])
        if self.trial.primary_sponsor is not None:
            langs.add(self.trial.primary_sponsor.country.submission_language)

        for rc in self.trial.recruitment_country.all():
            langs.add(rc.submission_language)

        return langs.intersection(set(settings.MANAGED_LANGUAGES))

    def get_trans_languages(self):
        return self.get_mandatory_languages() - set([self.language])

    def get_secondary_language(self):
        sec = None
        for lang in self.get_mandatory_languages():
            # fixme: get from settings
            if lang != 'en':
                sec = lang.lower()
                break
        return sec

    def get_absolute_url(self):
        # TODO: use reverse to replace absolute path
        return '/accounts/submission/%s/' % self.id

    def get_fields_status(self):
        if not getattr(self, '_fields_status', None):
            self._fields_status = pickle.loads(self.fields_status.encode('utf-8'))

        return self._fields_status

class RecruitmentCountry(models.Model):
    class Meta:
        verbose_name_plural = _('Recruitment Countries')

    submission = models.ForeignKey(Submission)
    country = models.ForeignKey(CountryCode, verbose_name=_('Country'), related_name='submissionrecruitmentcountry_set')

class Attachment(models.Model):
    class Meta:
        verbose_name_plural = _('Attachments')
    file = models.FileField(_('File'), upload_to=settings.ATTACHMENTS_PATH)
    description = models.TextField(_('Description'),blank=True,max_length=8000)
    submission = models.ForeignKey(Submission)
    public = models.BooleanField(_('Public'))

    def get_relative_url(self):
        return self.file.url.replace(settings.PROJECT_PATH, u'')

REMARK_STATUS = [
    # initial state, as created by reviewer
    ('opened', _('Opened')),
    # marked as noted by user
    ('acknowledged', _('Acknowledged')),
    # final state, after reviewer verifies changes by the user
    ('closed', _('Closed')),
]

REMARK_TRANSITIONS = {
    'opened':['acknowledged'],
    'acknowledged':['closed','opened'],
    'closed':[],
}

class RemarksOpened(models.Manager):
    def get_query_set(self):
        return super(RemarksOpened, self).get_query_set().filter(status__exact='opened')

class RemarksAcknowledged(models.Manager):
    def get_query_set(self):
        return super(RemarksAcknowledged, self).get_query_set().filter(status__exact='acknowledged')

class RemarksClosed(models.Manager):
    def get_query_set(self):
        return super(RemarksClosed, self).get_query_set().filter(status__exact='closed')

class Remark(models.Model):
    ''' A reviewer comment regarding a submission field.

    The remark is directed at the field identified by the context attribute.
    '''
    creator = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(default=datetime.now, editable=False)
    submission = models.ForeignKey(Submission)
    context = models.CharField(_('Context'), max_length=256, blank=True)
    text = models.TextField(_('Text'), max_length=2048)
    status = models.CharField(_('Status'), max_length=16, choices=REMARK_STATUS,
                              default=REMARK_STATUS[0][0])

    objects = models.Manager()
    opened = RemarksOpened()
    acknowledged = RemarksAcknowledged()
    closed = RemarksClosed()

    def __unicode__(self):
        return '%s:%s' % (self.pk, self.submission_id)

    def short_text(self):
        return safe_truncate(self.text, 60)

NEWS_STATUS = [
    ('pending', _('Pending')),
    ('published', _('Published')),
]

class News(models.Model):

    class Meta:
        verbose_name_plural = _('News')

    title = models.CharField(_('Title'), max_length=256)
    text = models.TextField(_('Text'), max_length=2048)
    created = models.DateTimeField(default=datetime.now, editable=False)
    creator = models.ForeignKey(User, related_name='news_creator', editable=False)
    status = models.CharField(_('Status'), max_length=16, choices=NEWS_STATUS,
                              default=NEWS_STATUS[0][0])

    def short_title(self):
        return safe_truncate(self.title, 120)
        
    def short_text(self):
        return safe_truncate(self.text, 240)
    
    def __unicode__(self):
        return '%s' % (self.short_title())

# SIGNALS
def create_user_profile(sender, instance,**kwargs):
    UserProfile.objects.get_or_create(user=instance)
    
post_save.connect(create_user_profile, sender=User)
