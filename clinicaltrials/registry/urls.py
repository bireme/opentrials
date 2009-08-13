from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'add/$', 'clinicaltrials.registry.views.add'),   
    (r'$', 'clinicaltrials.registry.views.index'),    
)
