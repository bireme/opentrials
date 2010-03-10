from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^getterm/(?P<lang>[a-z]{2,2})/(?P<code>[A-Z](\d{2,2}(\.\d{3,3})*)?)?$', getterm, name='decs.getterm'),
    url(r'^search/(?P<lang>[a-z]{2,2})/(?P<prefix>[14]0[1-7])/(?P<term>.*)$', search),
    url(r'^search/(?P<lang>[a-z]{2,2})/(?P<term>.*)$', search, name='decs.search'),
    url(r'^test_search/$', test_search),
)
