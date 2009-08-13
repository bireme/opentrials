from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^clinicaltrials/', include('clinicaltrials.foo.urls')),

    # Django admin application and documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # Registry application
    (r'^clinicaltrials/$', 'clinicaltrials.registry.views.index'),    
    (r'^clinicaltrials/add/$', 'clinicaltrials.registry.views.add'),
    
)
