from django.conf.urls.defaults import *

from rebrac.views import index, user_dump

urlpatterns = patterns('',
    (r'^u/$', user_dump),    
    (r'^$', index),    
)
