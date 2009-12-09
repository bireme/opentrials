from django.db import models
from django.utils.translation import ugettext as _

#import datetime

#from utilities import safe_truncate

#from vocabulary.models import CountryCode, StudyPhase, StudyType, RecruitmentStatus, InterventionCode

#import choices

class Ticket(models.Model):
    date_registration = models.DateField(_('Date of Registration'), null=True,
                                         editable=False, db_index=True)
    date_iteration = models.DateField(_('Date of Iteration'), null=True,
                                         db_index=True)
    subject = models.TextField(_('Subject'), max_length=256, db_index=True)
    description = models.TextField(_('Description'), max_length=2000)
    owner = models.TextField(_('Request Owner'), max_length=256, db_index=True)
    from_user = models.TextField(_('From user'), max_length=256, db_index=True)
    to_user = models.TextField(_('To User'), max_length=256, db_index=True)
    status = models.TextField(_('Ticket Status'), max_length=256, db_index=True)
    #parent_relation = models.

#    class Meta:
 #       order_with_respect_to = 'trial'

    def __unicode__(self):
        return u'%s' % (self.subject)
