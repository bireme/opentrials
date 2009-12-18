from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from tickets.models import Ticket
from tickets.views import index, new_iteration, reopen_ticket, resolve_ticket, close_ticket, open_ticket


info_dict = {
    'queryset': Ticket.objects.all(),
}

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^list/$', object_list, info_dict),
    url(r'^history/(?P<object_id>\d+)/$', object_detail, info_dict, name='ticket.history' ),
    url(r'^open/(?P<context>\w+)/(?P<type>\w+)/$', open_ticket, name='ticket.open' ),
    url(r'^reopen/(?P<object_id>\d+)/$', reopen_ticket, name='ticket.reopen' ),
    url(r'^resolve/(?P<object_id>\d+)/$', resolve_ticket, name='ticket.resolve' ),
    url(r'^close/(?P<object_id>\d+)/$', close_ticket, name='ticket.close' ),
    url(r'^newiteration/(?P<object_id>\d+)/$', new_iteration, name='ticket.new_iteration' ),
)
