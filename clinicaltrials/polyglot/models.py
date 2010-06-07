from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Translation(models.Model):
    language = models.CharField(_('Language'), max_length=8,
                                blank=False, null=False, db_index=True,
                                choices=settings.TARGET_LANGUAGES)
    # standard fields to link to any other model
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    class Meta:
        abstract = True
        unique_together = (('content_type','object_id','language'),)

    def __unicode__(self):
        return self.language
    
    def natural_key(self):
        return self.content_type.natural_key()+ \
               self.content_object.natural_key()+ \
               (self.language, )

    @staticmethod
    def missing(content_object):
        ''' returns missing translation codes for a content object'''
        targets = set(value for value, label in settings.TARGET_LANGUAGES)
        done = set(t.language for t in content_object.translations.all())
        return targets-done

def get_multilingual_fields(model):
    """Returns a list of fields are begin translated for a given model class"""

    # Gets translation model from generic relation
    try:
        trans_model = model.translations.field.rel.to
    except AttributeError:
        # Unrecognized class or field
        return

    try:
        return trans_model.get_multilingual_fields()
    except AttributeError:
        return [field.name for field in trans_model._meta.fields if field.name not in ('id','language','content_type','object_id')]

