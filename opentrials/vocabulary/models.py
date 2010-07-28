############################################ Controlled Vocabularies ###

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from polyglot.models import Translation

class SimpleVocabularyManager(models.Manager):
    def get_by_natural_key(self, label):
        return self.get(label=label)

class SimpleVocabulary(models.Model):
    objects = SimpleVocabularyManager()
    
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.TextField(_('Description'), max_length=2000,
                                   blank=True)
    translations = generic.GenericRelation('VocabularyTranslation')

    class Meta:
        abstract = True
        ordering = ['id']

    def __unicode__(self):
        return self.label
    
    def natural_key(self):
        return (self.label,)

    @classmethod
    def choices(cls):
        return ( (term.id, term.label) for term in cls.objects.all() )

class VocabularyTranslation(Translation):
    # same as SimpleVocabulary, except for unique=False
    label = models.CharField(_('Label'), max_length=255, unique=False)
    description = models.TextField(_('Description'), max_length=2000,
                                   blank=True)

class CountryCode(SimpleVocabulary):
    ''' TRDS 11, Countries of Recruitment
        also used for Contacts and Institutions
    '''
    submission_language = models.CharField(_('Submission Language'), max_length=10, blank=True)

    class Meta:
        ordering = ['description']

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
    ''' TRDS 15a '''

class StudyPurpose(SimpleVocabulary):
    ''' TRDS 15b '''

class InterventionAssigment(SimpleVocabulary):
    ''' TRDS 15b '''

class StudyMasking(SimpleVocabulary):
    ''' TRDS 15b '''

class StudyAllocation(SimpleVocabulary):
    ''' TRDS 15b '''

class StudyPhase(SimpleVocabulary):
    ''' TRDS 15c '''

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


