from django.db import models, connection
from django.core.management.color import no_style
from django.contrib.contenttypes import generic
from django.db.models.sql.query import setup_join_cache

from deleting.models import ControlledDeletion

class MyClass(ControlledDeletion):
    class Meta:
        app_label = 'temporary_test'

    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=2000, blank=True)

setup_join_cache(MyClass)

def create_tables():
    cursor = connection.cursor()
    style = no_style()
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)

    sql, references = connection.creation.sql_create_model(MyClass, style, seen_models)

    pending_references = {}
    for refto, refs in references.items():
        pending_references.setdefault(refto, []).extend(refs)
        if refto in seen_models:
            sql.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))
    sql.extend(connection.creation.sql_for_pending_references(MyClass, style, pending_references))
    for statement in sql:
        cursor.execute(statement)

