from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from django.contrib.auth.views import password_reset, password_reset_done
from django.contrib.auth.views import password_reset_complete, password_reset_confirm
from django.views.generic.list_detail import object_list, object_detail

from reviewapp.views import index, user_dump, new_submission, submissions_list
from reviewapp.views import reviewlist, new_submission_from_trial
from reviewapp.views import dashboard, submission_detail, user_profile
from reviewapp.views import upload_trial, open_remark, resend_activation_email
from reviewapp.views import change_remark_status, delete_remark
from reviewapp.views import contact, submission_delete, change_submission_status
from reviewapp.views import news_list, news_detail

from reviewapp.models import Submission


submissions = {
   'queryset':Submission.objects.all()
}

urlpatterns = patterns('',

    url(r'^news/$', news_list, name='reviewapp.newslist'),
    
    url(r'^news/(?P<object_id>\d+)/$', news_detail, name='reviewapp.news'),

    url(r'^accounts/dashboard/$', dashboard, name='reviewapp.dashboard'),

    url(r'^accounts/profile/$', user_profile, name='reviewapp.userhome'),

    url(r'^accounts/uploadtrial/$', upload_trial, name='reviewapp.uploadtrial'), #same as accounts/profile

    url(r'^accounts/submissionlist/$', submissions_list, name='reviewapp.submissionlist'), #same as accounts/profile
    url(r'^accounts/reviewlist/$', reviewlist, name='reviewapp.reviewlist'),

    url(r'^accounts/submission/(\d+)/$', submission_detail, 
        name='reviewapp.submission'),
        
    url(r'^accounts/submission/delete/(\d+)/$', submission_delete, 
        name='reviewapp.submission_delete'),
        
    url(r'^accounts/submission/change/(?P<submission_pk>\d+)/(?P<status>[a-z]+)/$', change_submission_status,
        name='reviewapp.change_submission_status'),

    url(r'^accounts/newsubmission/$', new_submission,
        name='reviewapp.new_submission'),

    url(r'^accounts/newsubmission-from-trial/(\w+)/$', new_submission_from_trial,
        name='reviewapp.new_submission_from_trial'),

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
        
    url(r'^contact/$', contact, name='reviewapp.contact'),

    url(r'^remark/change/(?P<remark_id>\d+)/(?P<status>[a-z]+)/$', change_remark_status,
        name='reviewapp.changeremarkstatus'),
        
    url(r'^remark/delete/(?P<remark_id>\d+)/$', delete_remark,
        name='reviewapp.delete_remark'),
        
    url(r'^$', index, name='reviewapp.home'),  
)
