import datetime

from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.loading import get_app, get_models
from django.template.defaultfilters import slugify

from repository.models import ClinicalTrial
from repository import choices

from vocabulary.models import CountryCode, InterventionCode, StudyPurpose
from vocabulary.models import InterventionAssigment, StudyMasking, StudyAllocation
from vocabulary.models import StudyPhase, StudyType

VALID_FUNCTIONS = (
    'xml_ictrp',
    'xml_opentrials',
    'xml_opentrials_dtd',
    'xml_opentrials_mod',
    'xml_opentrials_minimal_sample',
    'xml_opentrials_full_sample',
    )

def xml_ictrp(trial, **kwargs):
    """Generates an ICTRP XML for a given Clinical Trial and returns as string."""
    return render_to_string(
            'repository/xml/xml_ictrp.xml', # old clinicaltrial_detail.xml
            {'object': trial, 'reg_name': settings.REG_NAME},
            )

def xml_opentrials(trial, **kwargs):
    """Generates an Opentrials XML for a given Clinical Trial and returns as string."""
    return render_to_string(
            'repository/xml/xml_opentrials.xml',
            {'object': trial, 'reg_name': settings.REG_NAME},
            )

DTD_TEMPLATE = """<!-- ===========================================================================
File: opentrials.dtd

OpenTrials: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: %(generation)s

This DTD depends on the opentrials-vocabularies.mod definitions file.

See:
http://reddes.bvsalud.org/projects/clinical-trials/wiki/RegistrationDataModel

Partially based on the WHO ICTRP XML DTD, http://www.who.int/ictrp
DTD Version 1.0: 2008-04-23 (with changes up to and including 2008-09-15)
Most element names are the same. Structure is different, with more validation
in the form of attribute enumerations. Also, this is intended to represent a
single trial record.

Comments:
  - "formset n/9" refer to each of the 9 trial submission forms
  - "TRDS n (x..y)": field number in the ICTRP Trial Registration Data Set
                     (x..y) indicate element multiplicity in UML notation
=========================================================================== -->

%(entities)s"""

def xml_opentrials_dtd(**kwargs):
    """
    This function doesn't really works. It is just to compare existing fields
    with current standard while I work on the definitions (Marinho Brandao)
    """
    entities = []

    # Vocabularies
    entities.append('\n'.join([
            '<!ENTITY % vocabularies SYSTEM "opentrials-vocabularies.mod">',
            '%vocabularies;'
            ]))

    # QUESTIONS:
    #  - should we support translations?
    #  - what's the field 'utn'?
    #  - what's most important: keep as possible the current standard or keep accuracy of field names?

    trial_tree = {
        'trial_identification':
            {'elements': [
                'scientific_title', 'scientific_acronym?', 'public_title?', 'acronym?',
                ('utn?', 'utrn_number'),
                ('opentrials_id?', 'trial_id'),
                ('secondary_ids*', 'trialnumber_set'),
                ],
            },
        'sponsors_and_support': 
            {'elements': [
                'primary_sponsor',
                ('secondary_sponsor*', 'trialsecondarysponsor_set'),
                ('source_support*', 'trialsupportsource_set'),
                ],
            },
        'health_conditions':
            {'elements': [
                ('freetext?', 'hc_freetext'),
                ('hc_code*', 'descriptor_set'),
                'keyword*'],
            },
        'interventions':
            {'elements': [
                ('freetext?', 'i_freetext'),
                ('i_code*', 'i_code'),
                'keyword*',
                ],
            },
        'recruitment':
            {'elements': [
                'recruitment_country+', 'inclusion_criteria', 'gender?',
                ('agemin?', 'agemin_value'),
                ('agemax?', 'agemax_value'),
                'exclusion_criteria?',
                ('date_enrolment_anticipated?', 'enrollment_start_planned'),
                ('date_enrolment_actual?', 'enrollment_start_actual'),
                ('target_size?', 'target_sample_size'),
                ],
            },
        'study': # old 'study_type'
            {'elements': [
                'study_design', 'phase', 'purpose', 'intervention_assignment',
                'masking', 'allocation',
                ],
             'attributes': ['language', 'expanded_access_program', 'number_of_arms'],
            },
        'outcomes':
            {'elements': [
                ('primary_outcome+', 'outcome_set'),
                ('secondary_outcome*', 'outcome_set')],
            },
        'contacts':
            {'elements': [
                ('public_contact', 'public_contact'),
                ('scientific_contact', 'scientific_contact'),
                ('site_contact?', 'sitecontact_set'),
                'person+'],
            },
        'references':
            {'elements': ['link*'],
            },
        'others':
            {'elements': [],
            },
        }

    # Collect fields from model class
    fields = ClinicalTrial._meta.fields
    m2m_fields = ClinicalTrial._meta.many_to_many[:-1]
    related = ClinicalTrial._meta.get_all_related_objects()
    related_fields = [item for item in related if item.name.startswith('repository:')]

    # Dictionary with all kinds of fields at once
    all_fields = {}
    all_fields.update(dict([(f.name, f) for f in fields]))
    all_fields.update(dict([(f.name, f) for f in m2m_fields]))
    all_fields.update(dict([(f.get_accessor_name(), f) for f in related_fields]))
    all_fields.pop('id');
    all_fields.pop('_deleted');
    all_fields.pop('exported')
    all_fields.pop('study_type')
    all_fields.pop('publiccontact_set')
    all_fields.pop('scientificcontact_set')
    pending_fields = all_fields.copy()

    clean = lambda w: w[:-1] if w[-1] in ('?','*','+') else w

    for el in reduce(lambda a,b: a+b, [i['elements'] + i.get('attributes', []) for i in trial_tree.values()]):
        tag, f_name = (clean(el[0]), el[1]) if isinstance(el, tuple) else (clean(el), clean(el))

        if f_name not in all_fields:
            print 'Field not found:', f_name
        else:
            pending_fields.pop(f_name, None)
    for f in pending_fields:
        print '-', f

    # Classes:
    # - ClinicalTrial
    # - TrialNumber 1/*
    # - TrialSecondarySponsor 1/*
    # - TrialSupportSource 1/*
    # - PublicContact 1/*
    # - ScientificContact 1/*
    # - SiteContact 1/*
    # - Outcome 1/*
    # - Descriptor 1/*
    # - Institution (by field)
    # - Contact (by field)

    return DTD_TEMPLATE%{
            'generation': datetime.date.today().strftime('%Y-%m-%d'),
            'entities': '\n\n'.join(entities),
            }

MOD_TEMPLATE = """<!-- ===========================================================================
File: opentrials-vocabularies.mod

OpenTrials: Latin-American and Caribbean Clinical Trial Record XML DTD
DTD Version 1.0: %(generation)s

Entity definitions used by the opentrials.dtd file.
This file should be generated automatically from controlled vocabulary data
such as those from Vocabulary application.
=========================================================================== -->

%(entities)s"""

def xml_opentrials_mod(**kwargs):
    """Generates the MOD file with valid vocabularies for Opentrials XML standard."""
    entities = []

    # Languages
    entities.append('\n'.join([
            '<!ENTITY % language.options',
            '    "en|es|fr|pt|other">'
            ]))

    # Health conditions
    entities.append('\n'.join([
            '<!-- TRDS 12: health condition attributes -->',
            '<!ENTITY % vocabulary.options',
            '    "decs|icd10|other">',
            ]))

    # Intervention codes
    icodes = map(slugify, InterventionCode.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 13: intervention descriptor attributes -->',
            '<!-- attribute options cannot contain slashes "/" -->',
            '<!ENTITY % interventioncode.options',
            '    "%s">' % '|'.join(icodes), # FIXME: check why labels were defined with
                                            # '-' replacing ' ' on old .mod
            ]))

    # Study statuses
    statuses = map(slugify, InterventionCode.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % studystatus.options',
            '    "%s">' % '|'.join(statuses),
            ]))

    # Age units
    entities.append('\n'.join([
            '<!ENTITY % ageunit.options',
            '    "null|years|months|weeks|days|hours">',
            ]))

    # Genders
    entities.append('\n'.join([
            '<!ENTITY % gender.options',
            '    "female|male|both">',
            ]))

    # Purposes
    purposes = map(slugify, StudyPurpose.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 15b: study_design attributes -->',
            '<!ENTITY % purpose.options',
            '    "%s">' % '|'.join(purposes),
            ]))

    # Assignment
    assignments = map(slugify, InterventionAssigment.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % assignment.options',
            '    "%s">' % '|'.join(assignments),
            ]))

    # Masking
    maskings = map(slugify, StudyMasking.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % masking.options',
            '    "%s">' % '|'.join(maskings),
            ]))

    # Allocation
    allocations = map(slugify, StudyAllocation.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % allocation.options',
            '    "%s">' % '|'.join(allocations),
            ]))

    # Phases
    phases = map(slugify, StudyPhase.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 15c -->',
            '<!ENTITY % phase.options',
            '    "%s">' % '|'.join(phases), # FIXME: replace N/A for null?
            ]))

    # Contact types
    entities.append('\n'.join([
            '<!ENTITY % contacttype.options',
            '    "public|scientific|site">',
            ]))

    # Countries
    countries = map(slugify, CountryCode.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % country.options',
            '    "%s">' % '|'.join(countries),
            ]))

    # Trial Statuses
    statuses = [st[0] for st in choices.TRIAL_RECORD_STATUS]
    entities.append('\n'.join([
            '<!ENTITY % trialstatus.options',
            '    "%s">' % '|'.join(statuses),
            ]))

    # Study Types
    study_types = map(slugify, StudyType.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % study_type.options',
            '    "%s">' % '|'.join(study_types),
            ]))

    return MOD_TEMPLATE%{
            'generation': datetime.date.today().strftime('%Y-%m-%d'),
            'entities': '\n\n'.join(entities),
            }

def xml_opentrials_minimal_sample(**kwargs):
    """
    Generates a basic minimal sample of OpenTrials XML standard, from:

        opentrials/repository/xml/opentrials.dtd

    The serialized data here is based on valid randomized data using fields from
    data model found in model classes.
    """
    pass

def xml_opentrials_full_sample(**kwargs):
    """
    Generates a full sample of OpenTrials XML standard, from:

        opentrials/repository/xml/opentrials.dtd

    The serialized data here is based on valid randomized data using fields from
    data model found in model classes.
    """
    pass

