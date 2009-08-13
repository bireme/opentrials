from django.conf.urls.defaults import *

from rebrac.views import index

urlpatterns = patterns('',
    (r'$', index),    
)
