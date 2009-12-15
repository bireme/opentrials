from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from tickets.models import Ticket
from tickets.views import index


info_dict = {
    'queryset': Ticket.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^list/$', object_list, info_dict),
    url(r'^history/(?P<object_id>\d+)/$', object_detail, info_dict ),
)
