# coding: utf-8
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


from rebrac.forms import SubmissionForm
from rebrac.models import Submission
from registry.models import ClinicalTrial, Institution

def index(request):
    username = request.user.username if request.user.is_authenticated() else None
    return render_to_response('rebrac/index.html', locals())

def user_dump(request):
    uvars = [{'k':k, 'v':v} for k, v in request.user.__dict__.items()]
    return render_to_response('rebrac/user_dump.html', locals())

def new_submission(request):
#    import pdb
#    pdb.set_trace()
#    
    if request.method == 'POST': # If the form has been submitted...
        form = SubmissionForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            pass
            trial = ClinicalTrial()            

            trial.scientific_title = request.POST.get('scientific_title')
            trial.primary_sponsor = Institution.objects.get(
                                         pk=request.POST.get('primary_sponsor'))

            trial.save()

            sub = Submission()
            sub.creator = request.user
            sub.trial = trial

            sub.save()           

            return HttpResponseRedirect(reverse('rebrac.userhome')) # Redirect after POST
    else:
        form = SubmissionForm() # An unbound form

    return render_to_response('rebrac/new_submission.html', {
        'form': form,
    })