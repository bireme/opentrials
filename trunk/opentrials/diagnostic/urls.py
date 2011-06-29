from django.conf.urls.defaults import *

from diagnostic.views import *

urlpatterns = patterns('',
    # Diagnostic views
    url(r'^smoke/$', smoke_test),
    url(r'^reqdump/$', req_dump),
    url(r'^sysinfo/$', sys_info),
    url(r'^error/$', raise_error),
    url(r'^dumpdb/$', export_database),
    url(r'^backupdb/$', backup_database, name='backup_database'),
    url(r'^dumpdata/(?P<appname>[a-z_]+)?/?$', dump_data, name='dumpdata'),
)
