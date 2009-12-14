from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime

class Category(models.Model):
    
    category = models.CharField(_('Category'), max_length=256)
    
    def __unicode__(self):
        return self.category


class Question(models.Model):

    category = models.ForeignKey(Category)
    question = models.TextField(_('Question'), max_length=2000)
    answer = models.TextField(_('Answer'), max_length=2000)
    created = models.DateTimeField(_('Date of Registration'),default=datetime.now,
        editable=False)

    def __unicode__(self):
        return self.question
    