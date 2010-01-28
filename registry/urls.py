from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from registry.models import ClinicalTrial
from registry.views import index
from registry.views3 import edit_trial_index, step_1
from registry.views2 import step_2, step_3, step_4, step_5, step_6, step_7, step_8

info_dict = {
    'queryset': ClinicalTrial.objects.all(),
}

info_dict_xml = {
    'queryset': ClinicalTrial.objects.all(),    
    'template_name': 'registry/clinicaltrial_detail.xml',
    'mimetype': 'text/xml',
}

urlpatterns = patterns('',
    url(r'^edit/(\d+)/$', edit_trial_index, name='edittrial'),
    url(r'^xml/(?P<object_id>\d+)/$', object_detail, info_dict_xml,
        name='registry.xml'),
    url(r'^step_1/(\d+)/$', step_1, name='registry.step_1'),
    url(r'^step_2/(\d+)/$', step_2, name='registry.step_2'),
    url(r'^step_3/(\d+)/$', step_3, name='registry.step_3'),
    url(r'^step_4/(\d+)/$', step_4, name='registry.step_4'),
    url(r'^step_5/(\d+)/$', step_5, name='registry.step_5'),
    url(r'^step_6/(\d+)/$', step_6, name='registry.step_6'),
    url(r'^step_7/(\d+)/$', step_7, name='registry.step_7'),
    url(r'^step_8/(\d+)/$', step_8, name='registry.step_8'),
    url(r'^$', index),
    url(r'^list/$', object_list, info_dict),
)
