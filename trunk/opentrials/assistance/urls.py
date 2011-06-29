from django.conf.urls.defaults import *

from assistance.views import faq
from assistance.models import Question

urlpatterns = patterns('',
    url(r'^faq/$', faq, name="assistance.faq"),
)
