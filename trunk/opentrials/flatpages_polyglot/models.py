from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes import generic

from polyglot.models import Translation

class FlatPageTranslation(Translation):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=2000, blank=True)

    def __unicode__(self):
        return self.title

FlatPage.translations = generic.GenericRelation(FlatPageTranslation)
FlatPage.translations.contribute_to_class(FlatPage, 'translations')

