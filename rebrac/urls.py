from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login, logout

from rebrac.views import index, user_dump

urlpatterns = patterns('',
    url(r'^accounts/profile/$', user_dump, name='rebrac.userhome'),    
    url(r'^accounts/login/$', login, 
        dict(template_name='rebrac/login.html'),
        name='rebrac.login'),
    url(r'^accounts/logout/$', logout, 
        dict(next_page='/'),
        name='rebrac.logout'),
    url(r'^$', index, name='rebrac.home'),  
)
