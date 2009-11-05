from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.contrib.auth.views import login, logout
from django.views.generic import list_detail

from rebrac.views import index, user_dump
from rebrac.models import Submission


submissions = {
   'queryset':Submission.objects.all()
}

urlpatterns = patterns('',
    url(r'^accounts/profile/$', list_detail.object_list,
        submissions, name='rebrac.userhome'),
    url(r'^accounts/submissionlist/$', list_detail.object_list,
        submissions, name='rebrac.submissionlist'), #same of accounts/profile
    url(r'^accounts/submission/(?P<object_id>\d+)/$', list_detail.object_detail,
        submissions, name='rebrac.submission'), #same of accounts/profile    
    url(r'^accounts/userdump/$', user_dump),
    url(r'^accounts/login/$', login, 
        dict(template_name='rebrac/login.html'),
        name='rebrac.login'),
    url(r'^accounts/logout/$', logout, 
        dict(next_page='/'),
        name='rebrac.logout'),
    url(r'^$', index, name='rebrac.home'),  
)
