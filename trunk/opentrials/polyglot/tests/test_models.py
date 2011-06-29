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

from django.db import models, connection
from django.core.management.color import no_style
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes import generic
from django.db.models.sql.query import setup_join_cache

from polyglot.models import Translation

class FlatPageTranslation(Translation):
    class Meta:
        app_label = 'temporary_test'

    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=2000, blank=True)

FlatPage.translations = generic.GenericRelation(FlatPageTranslation)
FlatPage.translations.contribute_to_class(FlatPage, 'translations')

class FlatPageRelative(models.Model):
    page = models.ForeignKey(FlatPage, related_name='page_relatives')
    information = models.TextField(blank=True)

setup_join_cache(FlatPageTranslation)
setup_join_cache(FlatPageRelative)

def create_tables():
    cursor = connection.cursor()
    style = no_style()
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)

    sql, references = connection.creation.sql_create_model(FlatPageTranslation, style, seen_models)
    new_sql, new_ref = connection.creation.sql_create_model(FlatPageRelative, style, seen_models)
    sql.extend(new_sql); references.update(new_ref)

    pending_references = {}
    for refto, refs in references.items():
        pending_references.setdefault(refto, []).extend(refs)
        if refto in seen_models:
            sql.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))
    sql.extend(connection.creation.sql_for_pending_references(FlatPageTranslation, style, pending_references))
    sql.extend(connection.creation.sql_for_pending_references(FlatPageRelative, style, pending_references))
    for statement in sql:
        cursor.execute(statement)

