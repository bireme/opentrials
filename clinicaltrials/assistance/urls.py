from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from assistance.models import Question, Category

info_dict = {
    'queryset': Question.objects.all().order_by('category', 'order'),
}

urlpatterns = patterns('',
    url(r'^faq/$', object_list, info_dict, name="assistance.faq"),
)
