from django.conf.urls.defaults import *

import utilities

from django.contrib import admin # Django admin UI 
admin.autodiscover()             # Django admin UI 

urlpatterns = patterns('',
    # Registry application
    url(r'^rg/', include('clinicaltrials.registry.urls')),

    # Tickets application
    url(r'^ticket/', include('clinicaltrials.tickets.urls')),

    # Assistance application
    url(r'^assistance/', include('clinicaltrials.assistance.urls')),

    # Review application
    url(r'^', include('clinicaltrials.reviewapp.urls')),

    # Django admin UI and documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # Diagnostic views
    url(r'^smoke/', utilities.smoke_test),
)

from django.conf import settings
if settings.DEBUG:
    # serve static files from develpment server
    from django.views import static
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
    