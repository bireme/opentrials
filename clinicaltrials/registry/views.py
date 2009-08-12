# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response
from clinicaltrials.registry.models import ClinicalTrial
from django.http import HttpResponse

def index(request):
    latest_clinicalTrials = ClinicalTrial.objects.all().order_by('dateFirst_enrollment')[:5]
    t = loader.get_template('registry/latest_clinicalTrials.html')
    c  = Context({
        'latest_clinicalTrials': latest_clinicalTrials,
    })
    return HttpResponse(t.render(c))

def add(request):
    #t = loader.get_template('registry/add_clinicalTrials.html')
    return render_to_response('registry/add_clinicalTrials.html') 