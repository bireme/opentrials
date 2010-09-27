# -*- encoding: utf-8 -*-

# polyglot: multilingual models, fields and widgets for Django
#
# Copyright (C) 2010 BIREME/PAHO/WHO
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

from django.contrib import admin
from django.contrib.contenttypes import generic
from django.conf import settings

from polyglot.models import Translation

class TranslationInline(generic.GenericStackedInline):
    max_num = len(settings.TARGET_LANGUAGES)
    radio_fields = {'language': admin.HORIZONTAL}

class TranslationAdmin(admin.ModelAdmin):
    def missing_translations(self, obj):
        return ' '.join(sorted(Translation.missing(obj)))

    def translation_completed(self, obj):
        return len(Translation.missing(obj)) == 0
    translation_completed.boolean = True
