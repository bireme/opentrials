from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

from datetime import datetime

from registry.models import ClinicalTrial

SUBMISSION_STATUS = [
    ('draft', 'draft'),
    ('pending', 'pending'),
    ('published', 'published'),
    ('rejected', 'rejected'),
]

class Submission(models.Model):
    creator = models.ForeignKey(User, related_name='creator', editable=False)
    created = models.DateTimeField(default=datetime.now, editable=False)
    updater = models.ForeignKey(User, null=True, related_name='updater', editable=False)
    updated = models.DateTimeField(null=True, editable=False)
    trial = models.OneToOneField(ClinicalTrial)
    status = models.CharField(_('Status'), max_length='64',
                              choices=SUBMISSION_STATUS,
                              default=SUBMISSION_STATUS[0][0])
    staff_note = models.TextField(_('Submission Note (staff use only)'), max_length=255,
                                    blank=True)

    def save(self):
        if self.id:
            self.updated = datetime.now()
        super(Submission, self).save()

    def short_title(self):
        return self.trial.short_title()

    def creator_username(self):
        return self.creator.username

    def __unicode__(self):
        return u'<%s> %s' % (self.creator_username(), self.short_title())

    def get_mandatory_languages(self):
        langs = set([u'EN'])
        langs.add(self.trial.primary_sponsor.country.language)
        
        for rc in self.trial.recruitmentcountry_set.all():
            langs.add(rc.country.language)
            
        return langs.intersection(settings.CHECKED_LANGUAGES)
