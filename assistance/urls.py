from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list
from assistance.models import Question

info_dict = {
    'queryset': Question.objects.all(),
}

urlpatterns = patterns('',
    url(r'^list/$', object_list, info_dict),
)
