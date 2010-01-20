from django.db import models
from django.utils.translation import ugettext_lazy as _

from utilities import safe_truncate

############################################ Controlled Vocabularies ###

class SimpleVocabulary(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000, 
                                   blank=True)
    class Meta:
        abstract = True
        ordering = ['id']

    def __unicode__(self):
        return self.label
          
    @classmethod
    def choices(cls):
        return ( (term.id, term.label) for term in cls.objects.all() )

class CountryCode(SimpleVocabulary):
    ''' TRDS 11, Countries of Recruitment 
        also used for Contacts and Institutions
    '''

    class Meta:
        ordering = ['description']

    language = models.CharField(_('Required Language'), max_length=2, blank=True)
    
    def __unicode__(self):
        return self.description
    
    @classmethod
    def choices(cls):
        return ( (cc.id, cc.description) for cc in cls.objects.all() )
    
class TrialNumberIssuingAuthority(SimpleVocabulary):
    ''' TRDS 3a '''
    class Meta:
        verbose_name_plural = _('Trial number issuing authorities')
        
    @classmethod
    def choices(cls):
        return ( (term.label, term.label) for term in cls.objects.all() )

class InterventionCode(SimpleVocabulary):
    ''' TRDS 18 '''

class StudyType(SimpleVocabulary):
    ''' TRDS 15 '''
    
class StudyPhase(SimpleVocabulary):
    ''' TRDS 15 '''
    
class RecruitmentStatus(SimpleVocabulary):
    ''' TRDS 18 '''

    class Meta:
        verbose_name_plural = _('Recruitment status')
    
class DecsDisease(SimpleVocabulary):
    ''' TRDS 12 '''
    
    def __unicode__(self):
        return self.description

class IcdChapter(SimpleVocabulary):
    ''' TRDS 12 '''
    
    def __unicode__(self):
        return self.description
        
class AttachmentType(SimpleVocabulary):
    ''' Types of documents attached to Clinical Trial records '''
        
