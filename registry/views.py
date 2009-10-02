# Create your views here.
from django.template import Context, loader
from django.shortcuts import render_to_response
from clinicaltrials.registry.models import ClinicalTrial
from django.http import HttpResponse
from django import forms
from django.utils.translation import ugettext as _

from django.contrib.admin.widgets import AdminDateWidget

def index(request):
    latest_clinicalTrials = ClinicalTrial.objects.all()[:5]
    t = loader.get_template('registry/latest_clinicalTrials.html')
    c  = Context({
        'latest_clinicalTrials': latest_clinicalTrials,
    })
    return HttpResponse(t.render(c))


def trial_registration_data_set(request):
    ''' TRDS view '''



class ClinicalTrialForm(forms.ModelForm):
    date_enrollment_anticipated = forms.DateTimeField(
        widget=AdminDateWidget(),
        label=ClinicalTrial._meta.get_field('date_enrollment_anticipated').verbose_name)

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