# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from clinicaltrials.tickets.models import Ticket, Followup
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse


from django import forms
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required
import choices

@login_required
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
        'username': request.user.username,
    })
    return HttpResponse(t.render(c))

@login_required
def waiting_acceptance(request):
    fw_waiting = Followup.objects.filter(status = 'new', ticket__type='review')
    t = loader.get_template('tickets/waiting_acceptance_tickets.html')
    c = Context({
        'fw_waiting': fw_waiting,
        'choices': choices,
        'username': request.user.username,
    })
    return HttpResponse(t.render(c))


@login_required
def reopen_ticket(request, object_id):
    ticket = get_object_or_404(Ticket, id=int(object_id))
    followup_latest = ticket.followup_set.latest()
    followup_new = Followup(ticket=ticket, status='reopened', description=followup_latest.description,
        subject=followup_latest.subject , reported_by=followup_latest.reported_by )
    followup_new.save();

    return HttpResponseRedirect(ticket.get_absolute_url())

@login_required
def close_ticket(request, object_id):
    ticket = get_object_or_404(Ticket, id=int(object_id))
    followup_latest = ticket.followup_set.latest()
    followup_new = Followup(ticket=ticket, status='closed', description=followup_latest.description,
        subject=followup_latest.subject , reported_by=followup_latest.reported_by )
    followup_new.save();

    return HttpResponseRedirect(ticket.get_absolute_url())

class FollowupParcForm(forms.Form):
    description = forms.CharField(label=_('Description'),widget=forms.Textarea)

@login_required
def resolve_ticket(request, object_id):
    if request.method == 'POST': # If the forms were submitted...
        form = FollowupParcForm(request.POST)
        if form.is_valid():
            desc = form.cleaned_data['description']
            ticket = get_object_or_404(Ticket, id=int(object_id))
            fw_lt = ticket.followup_set.latest()
            fw_nw = Followup(ticket=ticket, status='resolved',
                description=desc, subject=fw_lt.subject ,
                reported_by=fw_lt.reported_by, to_user=fw_lt.to_user, )
            fw_nw.save()
            
        return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        # recovering Ticket Data to input form fields
        followup_form = FollowupParcForm() # An unbound form
        return render_to_response('tickets/new_iteration.html', {
            'iteration_form': followup_form,
            'ticket_id': object_id,
            'mode': 'resolve',
            'username': request.user.username,
        })

@login_required
def accept_ticket(request, object_id):
    if request.method == 'POST': # If the forms were submitted...
        form = FollowupParcForm(request.POST)
        if form.is_valid():
            user =  request.user
            desc = form.cleaned_data['description']
            ticket = get_object_or_404(Ticket, id=int(object_id))
            fw_lt = ticket.followup_set.latest()
            fw_nw = Followup(ticket=ticket, status='accepted',
                description=desc, subject=fw_lt.subject ,
                reported_by=fw_lt.reported_by, to_user=user, )
            fw_nw.save()

        return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        # recovering Ticket Data to input form fields
        followup_form = FollowupParcForm() # An unbound form
        return render_to_response('tickets/new_iteration.html', {
            'iteration_form': followup_form,
            'ticket_id': object_id,
            'mode': 'accept',
            'username': request.user.username,
        })

@login_required
def new_iteration(request, object_id):
    ticket = get_object_or_404(Ticket, id=int(object_id))

    if request.method == 'POST': # If the forms were submitted...
        form = FollowupParcForm(request.POST)
        if form.is_valid():
            desc = form.cleaned_data['description']
            fw_lt = ticket.followup_set.latest()
            fw_nw = Followup(ticket=ticket, status=fw_lt.status,
                description=desc, subject=fw_lt.subject ,
                reported_by=fw_lt.reported_by, to_user=fw_lt.to_user, )
            fw_nw.save()

        return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        # recovering Ticket Data to input form fields
        iteration_form = FollowupParcForm() # An unbound form

    import pdb
    pdb.set_trace()

    return render_to_response('tickets/new_iteration.html', {
        'form': iteration_form,
        'ticket': ticket,
        'mode': 'newiteration',
        'username': request.user.username,
    })

class FollowupParcBForm(forms.Form):
    subject = forms.CharField(label=_('Subject'),required=True,max_length=256)
    description = forms.CharField(label=_('Description'),required=True ,widget=forms.Textarea)

@login_required
def open_ticket(request,context,type):
    if request.method == 'POST': # If the forms were submitted...
        form = FollowupParcBForm(request.POST)
        if form.is_valid():
            user =  request.user
            ticket = Ticket(context=context,type=type, creator=user, )
            ticket.save()
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            fw_nw = Followup(ticket=ticket , status='new',
                description=description, subject=subject ,
                reported_by=request.user, )
            fw_nw.save()

        return HttpResponseRedirect(ticket.get_absolute_url())
    else:
        # recovering Ticket Data to input form fields
        open_ticket_form = FollowupParcBForm() # An unbound form

    return render_to_response('tickets/open_ticket.html', {
        'open_ticket_form': open_ticket_form,
        'context': context,
        'type': type,
        'mode': 'open_ticket',
        'user_name': request.user.pk,
        'username': request.user.username,
    })