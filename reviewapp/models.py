from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from repository.models import ClinicalTrial, Institution
from vocabulary.models import CountryCode
from utilities import safe_truncate

from reviewapp.signals import create_user_profile
from django.db.models.signals import post_save

SUBMISSION_STATUS = [
    ('draft', 'draft'),
    ('pending', 'pending'),
    ('published', 'published'),
    ('rejected', 'rejected'),
]

ACCESS = [
    ('public', 'Public'),
    ('private', 'Private'),
]

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    preferred_language = models.CharField(_('Preferred language'),max_length=5,
                                choices=settings.MANAGED_LANGUAGES,
                                default=settings.MANAGED_LANGUAGES[-1][0])


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
    staff_note = models.TextField(_('Submission Note (staff use only)'), max_length=255,
                                    blank=True)

    def save(self):
        if self.id:
            self.updated = datetime.now()
        super(Submission, self).save()

    def short_title(self):
        return safe_truncate(self.title, 120)

    def creator_username(self):
        return self.creator.username

    def __unicode__(self):
        return self.short_title()

    def get_mandatory_languages(self):
        langs = set(['en'])
        langs.add(self.trial.primary_sponsor.country.submission_language)

        for rc in self.trial.recruitmentcountry_set.all():
            langs.add(rc.country.submission_language)

        return langs.intersection(set(settings.CHECKED_LANGUAGES))

    def get_absolute_url(self):
        # TODO: use reverse to replace absolute path
        return '/accounts/submission/%s/' % self.id

class RecruitmentCountry(models.Model):
    class Meta:
        verbose_name_plural = _('Recruitment Countries')

    submission = models.ForeignKey(Submission)
    country = models.ForeignKey(CountryCode, verbose_name=_('Country'), related_name='submissionrecruitmentcountry_set')

class Attachment(models.Model):
    class Meta:
        verbose_name_plural = _('Attachments')
    file = models.FileField(upload_to=settings.ATTACHMENTS_PATH)
    description = models.TextField(_('Description'),blank=True,max_length=8000)
    submission = models.ForeignKey(Submission)
    public = models.BooleanField(_('Public'))
    

REMARK_STATUS = [
    # initial state, as created by reviewer
    ('pending', _('Pending')),
    # marked as noted by user
    ('acknowledged', _('Acknowledged')),
    # final state, after reviewer verifies changes by the user
    ('verified', _('Verified')),
]

REMARK_TRANSITIONS = {
    'pending':['acknowledged', 'verified'],
    'acknowledged':['verified', 'pending'],
    'verified':['pending'],
}    
    
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
    
    def __unicode__(self):
        return '%s:%s' % (self.pk, self.submission_id)

post_save.connect(create_user_profile, sender=User)
