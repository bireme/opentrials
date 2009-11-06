from django.conf.urls.defaults import *
from django.views.generic import list_detail

from registry.models import ClinicalTrial

info_dict = {
    'queryset': ClinicalTrial.objects.all(),
}
info_dict_xml = {
    'queryset': ClinicalTrial.objects.all(),    
    'template_name': 'registry/clinicaltrial_detail.xml',
    'mimetype': 'text/xml',
}

urlpatterns = patterns('',
    url(r'^edit/(\d+)/$', 'clinicaltrials.registry.views.edit_trial_index'),
    url(r'^xml/(?P<object_id>\d+)/$', list_detail.object_detail, info_dict_xml,
        name='registry.xml'),
    url(r'^form/(\d+)/(\w+)/$', 'clinicaltrials.registry.views.edit_trial_form'),
    url(r'^$', 'clinicaltrials.registry.views.index'),
    url(r'^list/$', 'list_detail.object_list', info_dict),
)
