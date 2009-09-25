from django.db import models
from django.utils.translation import ugettext as _

from utilities import safe_truncate
import choices

################################################### Controlled Vocabularies ###

class StudyType(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000, 
                                   blank=True)

    def __unicode__(self):
        return self.label
    
class StudyPhase(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000,
                                   blank=True)

    def __unicode__(self):
        return self.label

class RecruitmentStatus(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000, 
                                   blank=True)

    class Meta:
        verbose_name_plural = _('Recruitment Status')
    
    def __unicode__(self):
        return self.label
    

