from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.views.generic.list_detail import object_list, object_detail

from reviewapp.views import index, user_dump, new_submission, submissions_list
from reviewapp.views import dashboard, submission_detail, user_profile

from reviewapp.models import Submission


submissions = {
   'queryset':Submission.objects.all()
}

urlpatterns = patterns('',
    url(r'^accounts/dashboard/$', dashboard, name='reviewapp.dashboard'),

    url(r'^accounts/profile/$', user_profile, name='reviewapp.userhome'),

    url(r'^accounts/submissionlist/$', submissions_list, name='reviewapp.submissionlist'), #same as accounts/profile

    url(r'^accounts/submission/(\d+)/$', submission_detail, 
        name='reviewapp.submission'),

    url(r'^accounts/newsubmission/$', new_submission,
        name='reviewapp.new_submission'),

    url(r'^accounts/userdump/$', user_dump),

    url(r'^accounts/login/$', login, dict(template_name='reviewapp/login.html',redirect_field_name='/'),
        name='reviewapp.login'),

    url(r'^accounts/logout/$', logout, dict(next_page='/'),
        name='reviewapp.logout'),
        
    url(r'^$', index, name='reviewapp.home'),  
)
