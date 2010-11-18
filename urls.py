# -*- encoding: utf-8 -*-

# OpenTrials: a clinical trials registration system
#
# Copyright (C) 2010 BIREME/PAHO/WHO, ICICT/Fiocruz e
#                    Ministério da Saúde do Brasil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls.defaults import *

import utilities

from django.contrib import admin # Django admin UI
admin.autodiscover()             # Django admin UI

urlpatterns = patterns('',
    # Repository application
    url(r'^rg/', include('opentrials.repository.urls')),

    # Tickets application
    url(r'^ticket/', include('opentrials.tickets.urls')),

    # Assistance application
    url(r'^assistance/', include('opentrials.assistance.urls')),

    # Review application
    url(r'^', include('opentrials.reviewapp.urls')),

    # Django admin UI and documentation
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^decs/', include('opentrials.decsclient.urls')),

    # django-registration views
    url(r'^accounts/', include('registration.urls')),

    # system diagnostic views (may be disabled in production)
    url(r'^diag/', include('opentrials.diagnostic.urls')),
    
    (r'^i18n/', include('django.conf.urls.i18n')),
)

from django.conf import settings
if settings.DEBUG:
    # serve static files from develpment server
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

