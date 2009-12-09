from django.conf.urls.defaults import *

from tickets.models import Ticket

info_dict = {
    'queryset': Ticket.objects.all(),
}

urlpatterns = patterns('',
#    url(r'^$', index),
 #   url(r'^list/$', object_list, info_dict),
)
