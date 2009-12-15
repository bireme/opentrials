# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from clinicaltrials.tickets.models import Ticket
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.forms.models import inlineformset_factory

from django import forms
from django.utils.translation import ugettext as _

from django.contrib.admin.widgets import AdminDateWidget

import choices

def index(request):
    user_tickets = Ticket.objects.all()[:5]
    user_open_tickets  = (i.opened_tickets() for i in Ticket.objects.all())
    user_close_tickets = (i.closed_tickets() for i in Ticket.objects.all())
    t = loader.get_template('tickets/user_tickets.html')
    c = Context({
        'user_tickets': user_tickets,
        'user_open_tickets': user_open_tickets,
        'choices': choices,
        'user_close_tickets': user_close_tickets,
    })
    return HttpResponse(t.render(c))