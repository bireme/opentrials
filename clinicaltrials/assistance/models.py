from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime

class Category(models.Model):
    class Meta:
        verbose_name_plural = _('Categories')

    label = models.CharField(_('Label'), max_length=255, unique=True)
    
    def __unicode__(self):
        return self.label


class Question(models.Model):

    category = models.ForeignKey(Category)
    title = models.TextField(_('Title'), max_length=2000)
    answer = models.TextField(_('Answer'), max_length=2000)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(_('Date of Registration'), default=datetime.now,
        editable=False)

    def save(self):
        super(Question, self).save()
        if self.order == 0:
            self.order = self.id*10
            self.save()

    def __unicode__(self):
        return self.title