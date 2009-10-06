from django.conf.urls.defaults import *
from clinicaltrials.registry.models import ClinicalTrial

info_dict = {
    'queryset': ClinicalTrial.objects.all(),
}


urlpatterns = patterns('',
    (r'^edit/(\d+)/$', 'clinicaltrials.registry.views.edit_trial_index'),   
    (r'^form/(\d+)/(\w+)/$', 'clinicaltrials.registry.views.edit_trial_form'),   
    (r'^$', 'clinicaltrials.registry.views.index'),
    (r'^list/$', 'django.views.generic.list_detail.object_list', info_dict),
)
