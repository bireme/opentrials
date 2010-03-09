from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from polyglot.models import Translation

from datetime import datetime

class Category(models.Model):
    class Meta:
        verbose_name_plural = _('Categories')

    label = models.CharField(_('Label'), max_length=255, unique=True)
    translations = generic.GenericRelation('CategoryTranslation')

    def __unicode__(self):
        return self.label

class CategoryTranslation(Translation):
    label = models.CharField(_('Label'), max_length=255, unique=True)

class Question(models.Model):
    category = models.ForeignKey(Category)
    title = models.TextField(_('Title'), max_length=255)
    answer = models.TextField(_('Answer'), max_length=2048)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(_('Date of Registration'), default=datetime.now,
        editable=False)
    translations = generic.GenericRelation('QuestionTranslation')

    def save(self):
        super(Question, self).save()
        if self.order == 0:
            self.order = self.id*10
            self.save()

    def __unicode__(self):
        return self.title

class QuestionTranslation(Translation):
    title = models.TextField(_('Title'), max_length=255)
    answer = models.TextField(_('Answer'), max_length=2048)

class FieldHelp(models.Model):
    class Meta:
        verbose_name_plural = _('Field Help')
        unique_together = ('form', 'field')
        ordering = ('id',)

    form = models.CharField(max_length=255, db_index=True)
    field = models.CharField(max_length=255, db_index=True)
    text = models.TextField(max_length=2048, blank=True)
    example = models.TextField(max_length=255, blank=True)

    translations = generic.GenericRelation('FieldHelpTranslation')

    def __unicode__(self):
        return self.text

class FieldHelpTranslation(Translation):
    text = models.TextField(max_length=2048, blank=True)
    example = models.TextField(max_length=255, blank=True)
