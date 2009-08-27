# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response
from clinicaltrials.registry.models import ClinicalTrial
from django.http import HttpResponse
from django import forms

def index(request):
    latest_clinicalTrials = ClinicalTrial.objects.all().order_by('dt_first_enrollment')[:5]
    t = loader.get_template('registry/latest_clinicalTrials.html')
    c  = Context({
        'latest_clinicalTrials': latest_clinicalTrials,
    })
    return HttpResponse(t.render(c))

#def add(request):
#    t = loader.get_template('registry/add_clinicalTrials.html')
#    return render_to_response('registry/add_clinicalTrials.html')
    
class ClinicalTrialForm(forms.ModelForm):
    class Meta:
        model = ClinicalTrial

def add(request):
    if request.method == 'POST':
        form = ClinicalTrialForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('registry/add_done.html', form.cleaned_data)
    else:
        form = ClinicalTrialForm()
    vars = {'form':form}
    return render_to_response('registry/add_clinicalTrials.html', vars)