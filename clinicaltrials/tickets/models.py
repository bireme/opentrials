from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from datetime import datetime
#from utilities import safe_truncate

import choices

class Ticket(models.Model):
    creator = models.ForeignKey(User, related_name='ticket_creator', editable=False)
    created = models.DateTimeField(_('Date of Registration'),default=datetime.now,
        editable=False)
    context = models.TextField(_('Context'), max_length=1,
        choices=choices.TICKET_CONTEXT, default=choices.TICKET_CONTEXT[0][0])

    def __unicode__(self):
        return u'%s' % (self.context[0][0])

    def save(self):
        self.updated = datetime.now()
        super(Ticket, self).save()

class Followup(models.Model):
    ticket = models.ForeignKey(Ticket)
    date_iteration = models.DateField(_('Date of Iteration'), null=True,
        db_index=True)
    subject = models.TextField(_('Subject'), max_length=256)
    description = models.TextField(_('Description'), max_length=2000)
    from_user = models.TextField(_('From user'), max_length=256, db_index=True)
    to_user = models.TextField(_('To User'), max_length=256, db_index=True)
    status = models.TextField(_('Ticket Status'), max_length=256, db_index=True)