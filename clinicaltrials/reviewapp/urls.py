from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.views.generic.list_detail import object_list, object_detail

from reviewapp.views import index, user_dump, new_submission, submissions_list
from reviewapp.views import dashboard, submission_detail, user_profile
from reviewapp.views import upload_trial, open_remark

from reviewapp.models import Submission, News


submissions = {
   'queryset':Submission.objects.all()
}

news = {
    'queryset': News.objects.filter(status__exact='published').order_by('-created',),
}

urlpatterns = patterns('',

    url(r'^news/$', object_list, news, name='reviewapp.newslist'),
    
    url(r'^news/(?P<object_id>\d+)/$', object_detail, news, name='reviewapp.news'),

    url(r'^accounts/dashboard/$', dashboard, name='reviewapp.dashboard'),

    url(r'^accounts/profile/$', user_profile, name='reviewapp.userhome'),

    url(r'^accounts/uploadtrial/$', upload_trial, name='reviewapp.uploadtrial'), #same as accounts/profile

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
        
    url(r'^remark/open/(?P<submission_id>\d+)/(?P<context>[a-zA-Z0-9_\- ]+)/$', open_remark,
        name='reviewapp.openremark'),

    url(r'^$', index, name='reviewapp.home'),  
)
