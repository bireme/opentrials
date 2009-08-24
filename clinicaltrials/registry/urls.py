from django.conf.urls.defaults import *
from clinicaltrials.registry.models import ClinicalTrial

info_dict = {
    'queryset': ClinicalTrial.objects.all(),
}


urlpatterns = patterns('',
    (r'^add/$', 'clinicaltrials.registry.views.add'),   
    (r'^$', 'clinicaltrials.registry.views.index'),
    (r'^list/$', 'django.views.generic.list_detail.object_list', info_dict),
)
