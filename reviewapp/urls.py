from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.contrib.auth.views import password_reset, password_reset_done
from django.contrib.auth.views import password_reset_complete, password_reset_confirm
from django.views.generic.list_detail import object_list, object_detail

from reviewapp.views import index, user_dump, new_submission, submissions_list
from reviewapp.views import dashboard, submission_detail, user_profile
from reviewapp.views import upload_trial, open_remark, resend_activation_email
from reviewapp.views import change_remark_status

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
        
    url(r'^accounts/resend/activation/email/$', resend_activation_email,
        name='reviewapp.resend_activation_email'),

    url(r'^accounts/password/reset/$', password_reset, {
        'template_name': 'reviewapp/password_reset_form.html',
        'email_template_name': 'reviewapp/password_reset_email.html',
        'post_reset_redirect': '/accounts/password/reset/done/'}, 
        name='reviewapp.password_reset'),

    url(r'^accounts/password/reset/done/$', password_reset_done, 
        {'template_name': 'reviewapp/password_reset_done.html'},
        name='reviewapp.password_reset_done'),
        
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {
        'template_name': 'reviewapp/password_reset_confirm.html',
        'post_reset_redirect': '/accounts/password/reset/complete/'},
        name='reviewapp.password_reset_confirm'),
        
    url(r'^accounts/password/reset/complete/$', password_reset_complete, 
        {'template_name': 'reviewapp/password_reset_complete.html'}, 
        name='reviewapp.password_reset_complete'),
        
    url(r'^remark/open/(?P<submission_id>\d+)/(?P<context>[a-zA-Z0-9_\- ]+)/$', open_remark,
        name='reviewapp.openremark'),

    url(r'^remark/change/(?P<remark_id>\d+)/(?P<status>[a-z]+)/$', change_remark_status,
        name='reviewapp.changeremarkstatus'),

    url(r'^$', index, name='reviewapp.home'),  
)
