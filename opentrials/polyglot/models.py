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

from django.db import models

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

def lang_format(lang): return lang[:2].lower()
CHOICES_TARGET_LANGUAGES = [(lang_format(value), label) for value, label in settings.TARGET_LANGUAGES]

class TranslationManager(models.Manager):
    def make_cache_key(self, model, object_id, lang):
        """Returns a string with the key used to store translation object in the cache.
        
        This is used also to do cache invalidation for this object when changed."""

        return 'polyglot:translation:%s.%s|%s|%s'%(
                model._meta.app_label, model.__name__, object_id, lang,
                )

    def get_translation_for_object(self, lang, obj=None, model=None, object_id=None,
            returns_default=False, create_if_not_exist=False):
        """Returns the translation object for a given object and language.
        
        Before call database, checks if there is a cached data for this."""

        # To make sure it is in format 'xx-xx'
        lang = lang_format(lang)

        # Gets object model and pk if informed
        if obj:
            model = type(obj)
            object_id = obj.pk

        cache_key = self.make_cache_key(model, object_id, lang)
        
        # Checks if there is a cached object for this
        from_cache = cache.get(cache_key, None)

        if from_cache:
            return from_cache

        # Gets the related content type
        c_type = ContentType.objects.get_for_model(model)

        # Gets the translation
        try:
            trans = self.get(language__iexact=lang, content_type=c_type, object_id=object_id)
        except ObjectDoesNotExist:
            if create_if_not_exist:
                trans = self.create(language=lang, content_type=c_type, object_id=object_id)
            elif returns_default:
                return obj
            else:
                raise

        # Stores in cache
        cache.set(cache_key, trans)

        # Returns the translation object
        return trans

class Translation(models.Model):
    language = models.CharField(_('Language'), max_length=8,
                                blank=False, null=False, db_index=True,
                                choices=CHOICES_TARGET_LANGUAGES)
    # standard fields to link to any other model
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = generic.GenericForeignKey()

    objects = TranslationManager()

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
        targets = set(value for value, label in CHOICES_TARGET_LANGUAGES)
        done = set(t.language for t in content_object.translations.all())
        return targets-done

    def save(self, *args, **kwargs):
        """This methods intercepts the 'save' method to force cache invalidation
        for this object"""

        self.language = lang_format(self.language)

        ret = super(Translation, self).save(*args, **kwargs)

        # Does cache invalidation
        cache_key = Translation.objects.make_cache_key(type(self), self.object_id, self.language)
        cache.set(cache_key, self)

        return ret

def get_multilingual_fields(model):
    """Returns a list of fields are begin translated for a given model class"""

    # Gets translation model from generic relation
    try:
        trans_model = model.translations.field.rel.to
    except AttributeError:
        try:
            trans_model = model.translations.rel.to
        except AttributeError, e:
            # Unrecognized class or field
            return []

    try: # customization hook, this try allows the
        return trans_model.get_multilingual_fields()
    except AttributeError:
        return [field.name for field in trans_model._meta.fields if field.name not in ('id','language','content_type','object_id')]

def get_ordered_languages(display_language, lower=False):
    """Returns available languages ordered according to display language given"""

    # Just sorts languages placing preferred language first
    languages = ([lang[0] for lang in settings.MANAGED_LANGUAGES_CHOICES if lang[0] == display_language] +
                 [lang[0] for lang in settings.MANAGED_LANGUAGES_CHOICES if lang[0] != display_language])
    languages = map(str, languages)

    if lower:
        languages = map(lambda s: s.lower(), languages)

    return languages

