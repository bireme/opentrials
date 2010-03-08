from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Translation(models.Model):
    language = models.CharField(_('Language'), max_length=8,
                                db_index=True,
                                choices=settings.TARGET_LANGUAGES)
    # standard fields to link to any other model
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    class Meta:
        abstract = True
        unique_together = (('content_type','object_id','language'),)

