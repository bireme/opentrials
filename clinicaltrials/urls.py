from django.conf.urls.defaults import *

import utilities

from django.contrib import admin # Django admin UI 
admin.autodiscover()             # Django admin UI 

urlpatterns = patterns('',
    # Registry application
    (r'^rg/', include('clinicaltrials.registry.urls')),

    # Rebrac public site application
    (r'^', include('clinicaltrials.rebrac.urls')),

    # Django admin UI and documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # Diagnostic views
    (r'^smoke/', utilities.smoke_test),
)
