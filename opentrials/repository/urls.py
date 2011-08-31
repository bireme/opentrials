from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from repository.models import ClinicalTrial

from repository.views import edit_trial_index, full_view, index, step_1, step_2, step_3
from repository.views import step_4, step_5, step_6, step_7, step_8, step_9, new_institution
from repository.views import trial_registered, trial_view, recruiting, trial_ictrp, trial_otxml
from repository.views import all_trials_ictrp, contacts, advanced_search, multi_otxml


urlpatterns = patterns('',
    url(r'^edit/(\d+)/$', edit_trial_index, name='repository.edittrial'),
    url(r'^view/(?P<trial_pk>\d+)/$', trial_view, name='repository.trialview'),
    url(r'^new_institution/$', new_institution, name='new_institution'),
    url(r'^contacts/$', contacts, name='contacts'),
    url(r'^step_1/(\d+)/$', step_1, name='step_1'),
    url(r'^step_2/(\d+)/$', step_2, name='step_2'),
    url(r'^step_3/(\d+)/$', step_3, name='step_3'),
    url(r'^step_4/(\d+)/$', step_4, name='step_4'),
    url(r'^step_5/(\d+)/$', step_5, name='step_5'),
    url(r'^step_6/(\d+)/$', step_6, name='step_6'),
    url(r'^step_7/(\d+)/$', step_7, name='step_7'),
    url(r'^step_8/(\d+)/$', step_8, name='step_8'),
    url(r'^step_9/(\d+)/$', step_9, name='step_9'),
    #public
    url(r'^recruiting/$', recruiting, name='repository.recruiting'),
    url(r'^advanced_search/$', advanced_search, name='repository.advanced_search'),
    url(r'^(?P<trial_fossil_id>[0-9A-Za-z-]+)/$', trial_registered, name='repository.trial_registered'),
    url(r'^(?P<trial_fossil_id>[0-9A-Za-z-]+)/xml/ictrp/$', trial_ictrp, name='repository.trial_ictrp'),
    url(r'^(?P<trial_fossil_id>[0-9A-Za-z-]+)/xml/ot/$', trial_otxml, name='repository.trial_otxml'),
    url(r'^(?P<trial_fossil_id>[0-9A-Za-z-]+)/v(?P<trial_version>\d+)/$', trial_registered, name='repository.trial_registered_version'),
    url(r'^(?P<trial_fossil_id>[0-9A-Za-z-]+)/v(?P<trial_version>\d+)/xml/ictrp/$', trial_ictrp, name='repository.trial_ictrp_version'),
    url(r'^(?P<trial_id>[0-9A-Za-z-]+)/v(?P<trial_version>\d+)/xml/opentrials/$', trial_otxml, name='repository.trial_otxml_version'),
    url(r'^all/xml/ictrp$', all_trials_ictrp),
    url(r'^multi/xml/ot', multi_otxml, name='repository.multi_otxml'),
    url(r'^$', index, name='repository.index'),
)
