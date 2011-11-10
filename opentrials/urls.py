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

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    
    #out of service page
    url(r'', direct_to_template, {
        'template': 'out_of_service.html'
    }),

)

