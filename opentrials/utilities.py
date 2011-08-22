#!/usr/bin/env python
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

from django.http import HttpResponse
from django.core import serializers

ELLIPSIS = u'\u2026'

def safe_truncate(text, max_length=60, ellipsis=ELLIPSIS, encoding='utf-8',
                  raise_exc=False):
    u'''truncate a string without breaking words

        >>> safe_truncate(u'the time has come', 9, u'>')
        u'the time>'
        >>> safe_truncate(u'the-time-has-come', 9, u'>')
        u'the-time>'
        >>> safe_truncate(u'the time', 8)
        u'the time'
        >>> safe_truncate(u'the time', 9)
        u'the time'
        >>> s = u'uncharacteristically-long'
        >>> safe_truncate(s, 10, u'>')
        u'uncharacteristically>'
        >>> safe_truncate(s, 10, u'>', raise_exc=True)
        Traceback (most recent call last):
          ...
        ValueError: Cannot safely truncate to 10 characters
    '''
    if not isinstance(text, unicode):
        text = text.decode(encoding)
    if len(text) <= max_length:
        return text
    # reverse-seek a non-alphanumeric character
    for i, c in enumerate(reversed(text[:max_length])):
        if not c.isalnum():
            pos = max_length - i - 1
            break
    else:
        pos = -1
    if pos == -1:
        if raise_exc:
            msg = 'Cannot safely truncate to %s characters'
            raise ValueError(msg % max_length)
        else:
            # seek nearest non-alphanumeric character after the cuttoff point
            pos = len(text)
            for i, c in enumerate(text[max_length:]):
                if not c.isalnum():
                    pos = max_length + i
                    break
            if pos == len(text):
                return text

    return text[:pos] + ellipsis

def export_json(modeladmin, request, queryset):
    response = HttpResponse(mimetype="application/json")
    serializers.serialize("json", queryset, stream=response, indent=2)
    return response
export_json.short_description = 'Export selected records in JSON format'

def user_in_group(user, group):
    return user.groups.filter(name=group).count() != 0 if user else False

def normalize_age(age, unit):
    "convert ages to hours"
    if unit == 'Y':
        return age*365*24
    elif unit == 'M':
        return age*30*24
    elif unit == 'W':
        return age*7*24
    elif unit == 'D':
        return age*24
    elif unit == 'H':
        return age
    return None


if __name__=='__main__':
    import doctest
    doctest.testmod()
