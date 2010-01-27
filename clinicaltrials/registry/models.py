from django.db import models, IntegrityError

from django.utils.translation import ugettext_lazy as _

from datetime import datetime
import string
from random import choice
from time import sleep

from utilities import safe_truncate

from vocabulary.models import CountryCode, StudyPhase, StudyType, RecruitmentStatus
from vocabulary.models import InterventionCode, TrialNumberIssuingAuthority

from registry import choices

# remove digits that look like letters and vice-versa
# remove vowels to avoid forming words
BASE28 = ''.join(d for d in string.digits+string.ascii_lowercase 
                   if d not in '1l0aeiou')
TRIAL_ID_PREFIX = 'RBR'
TRIAL_ID_DIGITS = 6
TRIAL_ID_TRIES = 3

def generate_trial_id(prefix, num_digits):
    s = choice(string.digits) # start with a numeric digit
    s += ''.join(choice(BASE28) for i in range(1, num_digits))
    return '-'.join([prefix, s[:num_digits/2], s[num_digits/2:]])

class ClinicalTrial(models.Model):
    # TRDS 1
    trial_id = models.CharField(_('Primary Id Number'), null=True, unique=True,
                                max_length=255, editable=False)
    # TRDS 2
    date_registration = models.DateField(_('Date of Registration'), null=True,
                                         editable=False, db_index=True)
    # TRDS 10a
    scientific_title = models.TextField(_('Scientific Title'),
                                        max_length=2000)
    # TRDS 10b
    scientific_acronym = models.CharField(_('Scientific Acronym'), blank=True,
                                          max_length=255)
    # TRDS 5
    primary_sponsor = models.OneToOneField('Institution', null=True, blank=True,
                                        verbose_name=_('Primary Sponsor'))
    # TRDS 9a
    public_title = models.TextField(_('Public Title'), blank=True,
                                    max_length=2000)
    # TRDS 9b
    acronym = models.CharField(_('Acronym'), blank=True, max_length=255)

    # TRDS 12a
    hc_freetext = models.TextField(_('Health Condition(s)'), blank=True,
                                   max_length=8000)
    # TRDS 13a
    i_freetext = models.TextField(_('Intervention(s)'), blank=True,
                                   max_length=8000)

    # TRDS 13b
    i_code = models.ManyToManyField(InterventionCode,
                                                through='TrialInterventionCode')

    # TRDS 14a
    inclusion_criteria = models.TextField(_('Inclusion Criteria'), blank=True,
                                          max_length=8000)
    # TRDS 14b
    gender = models.CharField(_('Gender (inclusion sex)'), max_length=1,
                              choices=choices.INCLUSION_GENDER,
                              default=choices.INCLUSION_GENDER[0][0])
    # TRDS 14c
    agemin_value = models.PositiveIntegerField(_('Inclusion Minimum Age'),
                                               default=0)
    agemin_unit = models.CharField(_('Minimum Age Unit'), max_length=1,
                                   choices=choices.INCLUSION_AGE_UNIT,
                                   default=choices.INCLUSION_AGE_UNIT[0][0])
    # TRDS 14d
    agemax_value = models.PositiveIntegerField(_('Inclusion Maximum Age'),
                                               default=0)
    agemax_unit = models.CharField(_('Maximum Age Unit'), max_length=1,
                                   choices=choices.INCLUSION_AGE_UNIT,
                                   default=choices.INCLUSION_AGE_UNIT[0][0])
    # TRDS 14e
    exclusion_criteria = models.TextField(_('Exclusion Criteria'), blank=True,
                                          max_length=8000)
    # TRDS 15a
    study_type = models.ForeignKey(StudyType, null=True, blank=True,
                                   verbose_name=_('Study Type'))

    # TRDS 15b
    study_design = models.TextField(_('Study Design'), blank=True,
                                          max_length=1000)
    # TRDS 15c
    phase = models.ForeignKey(StudyPhase, null=True, blank=True,
                              verbose_name=_('Study Phase'))

    # TRDS 16a,b (type_enrollment="anticipated")
    date_enrollment_anticipated = models.CharField( # yyyy-mm or yyyy-mm-dd
        _('Anticipated Date of First Enrollment'), max_length=10, blank=True)

    # TRDS 16a,b (type_enrollment="actual")
    date_enrollment_actual = models.CharField( # yyyy-mm or yyyy-mm-dd
        _('Actual Date of First Enrollment'), max_length=10, blank=True)

    # TRDS 17
    target_sample_size = models.PositiveIntegerField(_('Target Sample Size'),
                                                       default=0)
    # TRDS 18
    recruitment_status = models.ForeignKey(RecruitmentStatus, null=True, blank=True,
                                           verbose_name=_('Recruitment Status'))

    ################################### internal use, administrative fields ###
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(_('Last Update'), null=True, editable=False)
    exported = models.DateTimeField(null=True, editable=False)
    status = models.CharField(_('Status'), max_length=64,
                              choices=choices.TRIAL_RECORD_STATUS,
                              default=choices.TRIAL_RECORD_STATUS[0][0])
    staff_note = models.CharField(_('Record Note (staff use only)'),
                                  max_length='255',
                                  blank=True)

    class Meta:
        ordering = ['-updated',]

    def save(self):
        if self.id:
            self.updated = datetime.now()
        if self.status == choices.PUBLISHED_STATUS and not self.trial_id:
            for i in range(TRIAL_ID_TRIES):
                self.trial_id = generate_trial_id(TRIAL_ID_PREFIX, TRIAL_ID_DIGITS)
                try:
                    super(ClinicalTrial, self).save()
                except IntegrityError:
                    if i < TRIAL_ID_TRIES:
                        sleep(2**i) # wait to try again
                    else:
                        raise # all tries exhausted: give up
                else:    
                    break # no need to try again
        else:    
            super(ClinicalTrial, self).save()

    def identifier(self):
        return self.trial_id or '(req:%s)' % self.pk

    def short_title(self):
        if self.scientific_acronym:
            tit = u'%s - %s' % (self.scientific_acronym,
                                self.scientific_title)
        else:
            tit = self.scientific_title
        return safe_truncate(tit, 120)

    def __unicode__(self):
        return u'%s %s' % (self.identifier(), self.short_title())

    def trial_id_display(self):
        ''' return the trial id or an explicit message it is None '''
        if self.trial_id:
            return self.trial_id
        else:
            msg = 'not assigned (request #%)' % self.pk

    def record_status(self):
        return self.submission.status

    #TRDS 3 - Secondarty ID Numbers
    def trial_number(self):
        return self.trialnumber_set.all().select_related();

    # TRDS 4 - Source(s) of Monetary Support
    def support_sources(self):
        return self.trialsupportsource_set.all()

    # TRDS 6 - Secondary Sponsor(s)
    def secondary_sponsors(self):
        return self.trialsecondarysponsor_set.all()

    def updated_str(self):
        return self.updated.strftime('%Y-%m-%d %H:%M')
    updated_str.short_description = _('Updated')

    def related_contacts(self, relation):
        ''' return set of Contacts related to this trial with a
            given relationship
        '''
        return (r.contact for r in
                self.trialcontact_set.filter(relation=relation).select_related())

    def related_health_conditions(self, aspect, level):
        ''' return set of hc-code or keywords related to this trial with a
            given relationship
        '''
        return self.descriptor_set.filter(aspect=aspect, level=level).select_related()


    # TRDS 7 - Contact for Public Queries

    def public_contacts(self):
        ''' return set of Contacts related to this trial with
            relation='PublicContact'
        '''
        return self.related_contacts('PublicContact')

    # TRDS 8 - Contact for Scientific Queries

    def scientific_contacts(self):
        ''' return set of Contacts related to this trial with
            relation='ScientificContact'
        '''
        return self.related_contacts('ScientificContact')

    #TRDS 12b - HC-CODE
    def hc_code(self):
        ''' return set of HC-Code related to this trial with
            aspect = 'HealthCondition'
            level  = 'general'
        '''
        return self.related_health_conditions('HealthCondition','general')

    #TRDS 12c - HC-Keyword
    def hc_keyword(self):
        ''' return set of HC-Code related to this trial with
            aspect = 'HealthCondition'
            level  = 'specific'
        '''
        return self.related_health_conditions('HealthCondition','specific')
    
    #TRDS 13b - Invetion Code
    def intervention_code(self):
        ''' return set of Intervention Code related to this trial with
        '''
        return (r.i_code for r in
                self.trialinterventioncode_set.all().select_related())

    #TRDS 13c - Invention Keyword
    def intervention_keyword(self):
        ''' return set of Intervention Keyword related to this trial with
        '''
        return self.descriptor_set.filter(aspect='intervention').select_related()

    #TRDS 19 - Primary Outcomes
    def primary_outcomes(self):
        ''' return set of Primary Outcomes related to this trial with
        '''
        return self.outcome_set.filter(interest='primary').select_related()

    #TRDS 20 - Secondary Outcomes
    def secondary_outcomes(self):
        ''' return set of Secondary Outcomes related to this trial with
        '''
        return self.outcome_set.filter(interest='secondary').select_related()



################################### Entities linked to a Clinical Trial ###

# TRDS 3 - Secondary Identifying Numbers

class TrialNumber(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    issuing_authority = models.CharField(_('Issuing Authority'),
                                         max_length=255, db_index=True,
                                         choices=TrialNumberIssuingAuthority.choices())
    id_number = models.CharField(_('Secondary Id Number'),
                                max_length=255, db_index=True)

    def __unicode__(self):
        return u'%s: %s' % (self.issuing_authority, self.id_number)

# TRDS 6 - Secondary Sponsor(s)
class TrialSecondarySponsor(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    institution = models.ForeignKey('Institution')

    def __unicode__(self):
        return u'%s: %s' % (self.trial, self.institution)

# TRDS 4 - Source(s) of Monetary Support
class TrialSupportSource(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    institution = models.ForeignKey('Institution')

    def __unicode__(self):
        return u'%s: %s' % (self.trial, self.institution)

# TRDS 5 - Primary Sponsor

class Institution(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    address = models.TextField(_('Postal Address'), max_length=1500, blank=True)
    country = models.ForeignKey(CountryCode, verbose_name=_('Country'))

    def __unicode__(self):
        return safe_truncate(self.name, 80)

# TRDS 7 - Contact for Public Queries
# TRDS 8 - Contact for Scientific Queries

class Contact(models.Model):
    firstname = models.CharField(_('First Name'), max_length=50)
    middlename = models.CharField(_('Middle Name'), max_length=50, blank=True)
    lastname = models.CharField(_('Last Name'), max_length=50)
    email = models.EmailField(_('E-mail'), max_length=255)
    affiliation = models.ForeignKey(Institution, null=True, blank=True,
                                    verbose_name=_('Affiliation'))
    address = models.CharField(_('Address'), max_length=255, blank=True)
    city = models.CharField(_('City'), max_length=255, blank=True)
    country = models.ForeignKey(CountryCode, null=True, blank=True,
                                verbose_name=_('Country'),)
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
                            choices = choices.CONTACT_RELATION)
    status = models.CharField(_('Status'), max_length=255,
                            choices = choices.CONTACT_STATUS,
                            default = choices.CONTACT_STATUS[0][0])

    def __unicode__(self):
        return u'%s, %s: %s (%s)' % (self.relation, self.trial.short_title(),
                                     self.contact.name(), self.status)

# TRDS 11 - Countries of Recruitment

class RecruitmentCountry(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    country = models.ForeignKey(CountryCode, verbose_name=_('Country'))

    class Meta:
        verbose_name_plural = _('Recruitment Countries')

    def __unicode__(self):
        return self.country.description

# TRDS 13b - Intervention(s), intervention code

class TrialInterventionCode(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    i_code = models.ForeignKey(InterventionCode)

    class Meta:
        order_with_respect_to = 'trial'

    def __unicode__(self):
        return u'%s: %s' % (self.trial.short_title(), self.i_code.label)

# TRDS 19 - Primary Outcome(s)
# TRDS 20 - Key Secondary Outcome(s)

class Outcome(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    interest = models.CharField(_('Interest'), max_length=32,
                               choices=choices.OUTCOME_INTEREST,
                               default = choices.OUTCOME_INTEREST[0][0])
    description = models.TextField(_('Outcome Description'), max_length=8000)

    class Meta:
        order_with_respect_to = 'trial'

    def __unicode__(self):
        return safe_truncate(self.description, 80)

class Descriptor(models.Model):
    aspect = models.CharField(_('Trial Aspect'), max_length=255,
                        choices=choices.TRIAL_ASPECT)
    vocabulary = models.CharField(_('Vocabulary'), max_length=255,
                        choices=choices.DESCRIPTOR_VOCABULARY)
    version = models.CharField(_('Version'), max_length=64, blank=True)
    level = models.CharField(_('Level'), max_length=64,
                        choices=choices.DESCRIPTOR_LEVEL)
    code = models.CharField(_('Code'), max_length=255)
    text = models.CharField(_('Text'), max_length=255, blank=True)

    def __unicode__(self):
        return u'[%s] %s: %s' % (self.vocabulary, self.code, self.text)

class GeneralDescriptor(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    descriptor = models.ForeignKey(Descriptor)

    class Meta:
        order_with_respect_to = 'descriptor'

    def trial_identifier(self):
        return self.trial.identifier()

class SpecificDescriptor(models.Model):
    trial = models.ForeignKey(ClinicalTrial)
    descriptor = models.ForeignKey(Descriptor)

    class Meta:
        order_with_respect_to = 'descriptor'

    def trial_identifier(self):
        return self.trial.identifier()
