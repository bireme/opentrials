from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Registry application
    (r'^rg/', include('clinicaltrials.registry.urls')),

    # Rebrac public site application
    (r'^', include('clinicaltrials.rebrac.urls')),

    # Django admin application and documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),    
)
