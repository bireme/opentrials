from django.conf.urls.defaults import *
from icd10client.views import *

urlpatterns = patterns('',
    url(r'^get_chapters/$', get_chapters, name='icd10.get_chapters'),
    url(r'^search/(?P<lang>[a-z]{2,2})(-[a-z][a-z])?/(?P<prefix>\w+)/(?P<term>.*)$', search),
    url(r'^search/(?P<lang>[a-z]{2,2})(-[a-z][a-z])?/(?P<term>.*)$', search, name='icd10.search'),
    url(r'^test_search/$', test_search),
)
