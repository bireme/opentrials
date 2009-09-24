from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from utilities import safe_truncate

import vocabularies
   
class ClinicalTrial(models.Model):
    # TRDS 1
    trial_id = models.CharField(_('Primary Id Number'), null=True, unique=True,
                                max_length=255, editable=False)
    # TRDS 2
    date_registration = models.DateField(_('Date of Registration'), null=True, 
                                         editable=False, db_index=True)
    # TRDS 5
    primary_sponsor = models.ForeignKey('Institution', null=True,
                                        verbose_name=_('Primary Sponsor'))
    
    # TRDS 9a
    public_title = models.CharField(_('Public Title'), blank=True,
                                    max_length=2000)
    # TRDS 9b
    acronym = models.CharField(_('Acronym'), blank=True, max_length=255)
    
    # TRDS 10a
    scientific_title = models.CharField(_('Scientific Title'),
                                        max_length=2000)
    # TRDS 10b
    scientific_acronym = models.CharField(_('Scientific Acronym'), blank=True,
                                          max_length=255)
    # TRDS 12a
    hc_freetext = models.CharField(_('Health Condition(s)'), blank=True,
                                   max_length=8000)
    # TRDS 13a
    i_freetext = models.CharField(_('Intervention(s)'), blank=True,
                                   max_length=8000)
    # TRDS 14a
    inclusion_criteria = models.CharField(_('Inclusion Criteria'), blank=True,
                                          max_length=8000)
    # TRDS 14b
    gender = models.CharField(_('Gender (inclusion sex)'), max_length=1,
                              choices = vocabularies.INCLUSION_GENDER)
    # TRDS 14c
    agemin_value = models.PositiveIntegerField(_('Inclusion Minimum Age'),
                                               default=0)
    agemin_unit = models.CharField(_('Minimum Age Unit'), max_length=1,
                                   choices = vocabularies.INCLUSION_AGE_UNIT)
    # TRDS 14d
    agemax_value = models.PositiveIntegerField(_('Inclusion Maximum Age'), 
                                               default=0)
    agemax_unit = models.CharField(_('Maximum Age Unit'), max_length=1,
                                   choices = vocabularies.INCLUSION_AGE_UNIT)
    # TRDS 14e
    exclusion_criteria = models.CharField(_('Exclusion Criteria'), blank=True, 
                                          max_length=8000)
    # TRDS 15a
    study_type = models.ForeignKey('StudyType', verbose_name=_('Study Type'))

    # TRDS 15b
    study_design = models.CharField(_('Study Design'), blank=True, 
                                          max_length=1000)

    # TRDS 15c
    phase = models.ForeignKey('StudyPhase', verbose_name=_('Study Phase'), 
                              null=True)
    
    # TRDS 16a,b (type_enrollment="anticipated")
    date_enrollment_anticipated = models.CharField( # yyyy-mm or yyyy-mm-dd
        _('Anticipated Date of First Enrollment'), max_length=10)

    # TRDS 16a,b (type_enrollment="actual")
    date_enrollment_actual = models.CharField( # yyyy-mm or yyyy-mm-dd
        _('Actual Date of First Enrollment'), max_length=10)

    # TRDS 17
    target_sample_size = models.PositiveIntegerField(_('Target Sample Size'), 
                                                       default=0)
    # TRDS 18
    recruitment_status = models.ForeignKey('RecruitmentStatus', 
                                           verbose_name=_('Recruitment Status'))

    def identifier(self):
        return self.trial_id or '(#%s)' % self.pk
    
    def short_title(self):
        if self.scientific_acronym:
            tit = u'%s - %s' % (self.scientific_acronym, 
                                self.scientific_title)
        else:
            tit = self.scientific_title
        return safe_truncate(tit, 80)
        
    def __unicode__(self):
        return u'%s %s' % (self.identifier(), self.short_title())

    
    def related_institutions(self, relation):
        ''' return set of Institutions related to this trial with a 
            given relationship '''
        return (r.institution for r in 
                self.trial_institution_set.filter(relation=relation).select_related())
    
    # TRDS 4 - Source(s) of Monetary Support
    
    def support_sources(self):
        ''' return set of Institutions related to this trial with 
            relation='SupportSource'
        '''
        return self.related_institutions('SupportSource')
    
    # TRDS 6 - Secondary Sponsor(s)
    
    def secondary_sponsors(self):
        ''' return set of Institutions related to this trial with 
            relation='SecondarySponsor'
        '''
        return self.related_institutions('SecondarySponsor')

    
################################### Entities linked to a Clinical Trial ###    
    
# TRDS 3 - Secondary Identifying Numbers

class TrialNumber(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    issuing_authority = models.CharField(_('Issuing Authority'),
                                         max_length=255, db_index=True)
    id_number = models.CharField(_('Secondary Id Number'),
                                max_length=255, db_index=True)

    def __unicode__(self):
        return u'%s: %s' % (self.issuing_authority, self.trial_id)

# TRDS 4 - Source(s) of Monetary Support
# TRDS 6 - Secondary Sponsor(s)

class TrialInstitution(models.Model):    
    trial = models.ForeignKey(ClinicalTrial)
    institution = models.ForeignKey('Institution')
    relation = models.CharField(_('Relationship'), max_length=255,
                            choices = vocabularies.INSTITUTIONAL_RELATION)

    def __unicode__(self):
        return u'%s, %s: %s' % (self.relation, self.trial, self.institution)
    
# TRDS 5 - Primary Sponsor

class Institution(models.Model):
    name = models.CharField(_('Name'), max_length=2000)

    def __unicode__(self):
        return safe_truncate(self.name, 80)
        
# TRDS 7 - Contact for Public Queries
# TRDS 8 - Contact for Scientific Queries
    
class Contact(models.Model):
    firstname = models.CharField(_('First Name'), max_length=50)
    middlename = models.CharField(_('Middle Name'), max_length=50, blank=True)
    lastname = models.CharField(_('Last Name'), max_length=50)
    email = models.EmailField(_('Address'), max_length=255)
    affiliation = models.ForeignKey(Institution, verbose_name=_('Affiliation'),
                                    null=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=50, blank=True)
    country = models.CharField(_('Country'), max_length=50, blank=True)
    zip = models.CharField(_('Postal Code'), max_length=50, blank=True)
    telephone = models.CharField(_('Telephone'), max_length=255, blank=True)
    
    def name(self):
        names = self.firstname + u' ' + self.middlename + u' ' + self.lastname
        return u' '.join(names.split())
    
    def __unicode__(self):
        return self.name()

class TrialContact(models.Model):    
    trial = models.ForeignKey(ClinicalTrial)
    contact = models.ForeignKey(Contact)
    relation = models.CharField(_('Relationship'), max_length=255,
                            choices = vocabularies.CONTACT_RELATION)
    
    def __unicode__(self):
        return u'%s, %s: %s' % (self.relation, self.trial.short_title(), self.contact.name())
    
# TRDS 11 - Countries of Recruitment

class RecruitmentCountry(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    country = models.CharField(_('Country'), max_length=2, 
                               choices=vocabularies.COUNTRY)
    
    def __unicode__(self):
        return self.get_country_display()

# TRDS 19 - Primary Outcome(s)
# TRDS 20 - Keu Secondary Outcome(s)
    
class Outcome(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    description = models.CharField(_('Outcome Description'), max_length=8000)

    def __unicode__(self):
        return safe_truncate(self.description, 80)
    

################################################### Controlled Vocabularies ###

class Descriptor(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    aspect = models.CharField(_('Trial Aspect'), max_length=255, 
                        choices=vocabularies.TRIAL_ASPECT)
    vocabulary = models.CharField(_('Vocabulary'), max_length=255, 
                        choices=vocabularies.DESCRIPTOR_VOCABULARY)
    level = models.CharField(_('Level'), max_length=255, 
                        choices=vocabularies.DESCRIPTOR_LEVEL)
    code = models.CharField(_('Code'), max_length=255)
    text = models.CharField(_('Text'), max_length=255, 
                                       blank=True)

    def __unicode__(self):
        return self.label

class StudyType(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.CharField(_('Description'), max_length=2000, 
                                   blank=True)

    def __unicode__(self):
        return self.label
    
class StudyPhase(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.CharField(_('Description'), max_length=2000,
                                   blank=True)

    def __unicode__(self):
        return self.label

class RecruitmentStatus(models.Model):
    label = models.CharField(_('Label'), max_length=255, unique=True)
    description = models.CharField(_('Description'), max_length=2000, 
                                   blank=True)

    def __unicode__(self):
        return self.label
    
    