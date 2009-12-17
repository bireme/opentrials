# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from clinicaltrials.tickets.models import Ticket, Followup
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse


from django import forms
from django.utils.translation import ugettext as _

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

def reopen_ticket(request, object_id):
    ticket = get_object_or_404(Ticket, id=int(object_id))
    followup_latest = ticket.followup_set.latest()
    followup_new = Followup(ticket=ticket, status='reopened', description=followup_latest.description,
        subject=followup_latest.subject , reported_by=followup_latest.reported_by )
    followup_new.save();

    return HttpResponseRedirect(ticket.get_absolute_url())

class FollowupForm(forms.ModelForm):

    class Meta:
        model = Followup
        exclude = ['ticket',]




def new_iteration(request, object_id):
    if request.method == 'POST': # If the forms were submitted...
        ticket = get_object_or_404(Ticket, id=int(object_id))
        followup = Followup(ticket=ticket)
        iteration_form = FollowupForm(request.POST, instance=followup)
        if iteration_form.is_valid():
            iteration_form.save()
            return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        # recovering Ticket Data to input form fields
        iteration_form = FollowupForm() # An unbound form

    return render_to_response('tickets/new_iteration.html', {
        'iteration_form': iteration_form,
        'ticket_id': object_id,
    })

def new_ticket(request):
    return true