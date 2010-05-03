from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from datetime import datetime
#from utilities import safe_truncate

import choices

class Ticket(models.Model):
    class Meta:
        ordering = ['-created']
    
    creator = models.ForeignKey(User, related_name='ticket_creator', editable=False)
    created = models.DateTimeField(_('Date of Registration'),default=datetime.now,
        editable=False)
    context = models.CharField(_('Context'), max_length=256,
        choices=choices.TICKET_CONTEXT, default=choices.TICKET_CONTEXT[0][0], )
    type = models.CharField(_('Ticket Type'), max_length=256,
        choices=choices.TICKET_TYPE, default=choices.TICKET_TYPE[0][0], )

    @models.permalink
    def get_absolute_url(self):
        return ('ticket.history', [str(self.id)])


    def __unicode__(self):
        return u'%s' % (self.context)

    def save(self):
        self.updated = datetime.now()
        super(Ticket, self).save()

    def opened_tickets(self):
        ''' return set of Followups related to this ticket with a
            status = new or open
        '''
        return (r.followup for r in
                self.followup_set.filter(status="new").select_related())

    def is_closed(self):
        ''' return a boolean if the ticket is already close
        '''
        fw = self.followup_set.latest()
        return fw.status == "closed"

    def is_resolved(self):
        ''' return a boolean if the ticket is already resolved
        '''
        fw = self.followup_set.latest()
        return fw.status == "resolved"

    def reopen(self):
        ''' reopen tickect
        '''
        fw = self.followup_set.latest()
        fw.status = "reopened"
        return fw.status == "closed"

    def closed_tickets(self):
        ''' return set of Followups related to this ticket with a
            status = close
        '''
        return (r.followup for r in
                self.followup_set.filter(status="close").select_related())

class Followup(models.Model):
    ticket = models.ForeignKey(Ticket, db_index=True)
    iteration_date = models.DateTimeField(_('Date of Iteration'), db_index=True,
        editable=False, )
    subject = models.CharField(_('Subject'), max_length=256, db_index=True)
    description = models.TextField(_('Description'), max_length=2000, )
    reported_by = models.ForeignKey(User, related_name='ticket_reported_by',
        editable=False, null=True, blank=True, db_index=True, )
    to_user = models.EmailField(_('To User (e-mail)'), max_length=256, db_index=True,
        editable=False, null=True, blank=True )
    status = models.CharField(_('Ticket Status'), max_length=256,
        choices=choices.TICKET_STATUS, default=choices.TICKET_STATUS[0][0],
        db_index=True, )

    class Meta:
        get_latest_by = 'iteration_date'

    def save(self):
        self.iteration_date = datetime.now()
        super(Followup, self).save()


class Media(models.Model):
    followup = models.ForeignKey(Followup, related_name="ticket_media", null=True,
        blank=True, db_index=True, )
    file = models.FileField(_('Upload File'), blank=True, 
        upload_to='tickets_files', )