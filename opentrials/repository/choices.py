# coding: utf-8

from django.utils.translation import ugettext_lazy as _

## Qualifiers for the relationship of secondary entities with a ClinicalTrial #

INSTITUTIONAL_RELATION = [
    ('SupportSource', _('Source of monetary or material support')), #TRDS 4
    ('SecondarySponsor', _('Secondary sponsor')), #TRDS 6
]

CONTACT_RELATION = [
    ('PublicContact', _('Contact for Public Queries')), #TRDS 7
    ('ScientificContact', _('Contact for Scientific Queries')), #TRDS 8
    ('SiteContact', _('Contact for Site Queries')), #TRDS 8
]

CONTACT_STATUS = [
    ('Active', _('Active and current contact')),
    ('Inactive', _('Inactive or previous contact')),
]

OUTCOME_INTEREST = [
    ('primary', _('Primary')), # TRDS 19
    ('secondary', _('Secondary')), # TRDS 20
]

#################################################### Limited choices fields ###


TRIAL_RECORD_STATUS = [
    ('processing', _('processing')),
    ('published', _('published')),
    ('archived', _('archived')),
]
PROCESSING_STATUS = TRIAL_RECORD_STATUS[0][0]
PUBLISHED_STATUS  = TRIAL_RECORD_STATUS[1][0]
ARCHIVED_STATUS   = TRIAL_RECORD_STATUS[2][0]


INCLUSION_GENDER = [('-', _('both')), ('M', _('male')), ('F', _('female')),]

INCLUSION_AGE_UNIT = [
    ('-', _('no limit')),
    ('Y', _('years')),
    ('M', _('months')),
    ('W', _('weeks')),
    ('D', _('days')),
    ('H', _('hours')),
]

######################################################## Descriptor choices ###

TRIAL_ASPECT = [
    ('HealthCondition', _('Health Condition or Problem Studied')), #TRDS 12
    ('Intervention', _('Intervention')), #TRDS 13
]

DESCRIPTOR_LEVEL = [
    ('general', _('General')),
    ('specific', _('Specific')),
]

DESCRIPTOR_VOCABULARY = [
    ('DeCS', _('DeCS: Health Sciences Descriptors')),
    ('ICD-10', _('ICD-10: International Classification of Diseases (10th. rev.)')),
    ('CAS', _('Chemical Abstracts Service')),
]
