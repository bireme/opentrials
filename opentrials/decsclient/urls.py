from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^getterm/(?P<lang>[a-z]{2,2})(-[a-z][a-z])?/(?P<code>[A-Z](\d{2,2}(\.\d{3,3})*)?)?$', getterm, name='decs.getterm'),
    url(r'^getdescendants/(?P<code>[A-Z](\d{2,2}(\.\d{3,3})*)?)?$', getdescendants, name='decs.getdescendants'),
    url(r'^search/(?P<lang>[a-z]{2,2})(-[a-z][a-z])?/(?P<prefix>[14]0[1-7])/(?P<term>.*)$', search),
    url(r'^search/(?P<lang>[a-z]{2,2})(-[a-z][a-z])?/(?P<term>.*)$', search, name='decs.search'),
    url(r'^test_search/$', test_search),
)
