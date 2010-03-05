from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'^getterm/(?P<lang>[a-z]{2,2})/(?P<code>[A-Z](\d{2,2}(\.\d{3,3})*)?)?$', getterm),
    url(r'^search/(?P<lang>[a-z]{2,2})/(?P<term>.*)$', search),
)
