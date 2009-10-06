from django.db import models
from django.utils.translation import ugettext as _

from utilities import safe_truncate

################################################### Controlled Vocabularies ###

class SimpleVocabulary(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000, 
                                   blank=True)
    class Meta:
        abstract = True
        ordering = ['id']

    def __unicode__(self):
        return self.label
    
    def choice_label(self):
        ''' return the label to be used in (value, label) choice pairs '''
        return self.label
    
    @classmethod
    def choices(cls, limit=300):
        return ( (i.pk, i.choice_label()) for i in cls.objects.all()[:limit] )
        
class CountryCode(SimpleVocabulary):
    ''' TRDS 11, Countries of Recruitment 
        also used for Contacts and Institutions
    '''
    
    def __unicode__(self):
        return self.description
    
    choice_label = __unicode__
    
class InterventionCode(SimpleVocabulary):
    ''' TRDS 18 '''

class StudyType(SimpleVocabulary):
    ''' TRDS 15 '''
    
class StudyPhase(SimpleVocabulary):
    ''' TRDS 15 '''

class RecruitmentStatus(SimpleVocabulary):
    ''' TRDS 18 '''

    class Meta(SimpleVocabulary.Meta):
        verbose_name_plural = _('Recruitment status')
    

