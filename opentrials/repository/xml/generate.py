import datetime

from django.template.loader import render_to_string
from django.conf import settings

from repository import choices
from repository.xml import OPENTRIALS_XML_VERSION
from repository.templatetags.repository_tags import prep_label_for_xml

from vocabulary.models import CountryCode, InterventionCode, StudyPurpose
from vocabulary.models import InterventionAssigment, StudyMasking, StudyAllocation
from vocabulary.models import StudyPhase, StudyType, RecruitmentStatus, InstitutionType

VALID_FUNCTIONS = (
    'xml_ictrp',
    'xml_opentrials',
    'xml_opentrials_mod',
    )

def xml_ictrp(trial, **kwargs):
    """Generates an ICTRP XML for a given Clinical Trial and returns as string."""
    return render_to_string(
            'repository/xml/xml_ictrp.xml', # old clinicaltrial_detail.xml
            {'object': trial, 'reg_name': settings.REG_NAME},
            )

def xml_opentrials(trial, persons, include_translations=True, **kwargs):
    """Generates an Opentrials XML for a given Clinical Trial and returns as string."""

    for translation in trial.translations:
        translation['primary_outcomes'] = []
        for outcome in trial.primary_outcomes:
            for out_trans in outcome['translations']:
                if out_trans['language'] == translation['language']:
                    translation['primary_outcomes'].append(out_trans)

        translation['secondary_outcomes'] = []
        for outcome in trial.secondary_outcomes:
            for out_trans in outcome['translations']:
                if out_trans['language'] == translation['language']:
                    translation['secondary_outcomes'].append(out_trans)

    return render_to_string(
            'repository/xml/xml_opentrials.xml',
            {'object': trial,
             'reg_name': settings.REG_NAME,
             'persons': persons,
             'include_translations': include_translations,
             'opentrials_xml_version': OPENTRIALS_XML_VERSION},
            )

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
    #entities.append('\n'.join([
    #        '<!ENTITY % language.options',
    #        '    "en|es|fr|pt|other">'
    #        ]))

    # Health conditions
    entities.append('\n'.join([
            '<!-- TRDS 12: health condition attributes -->',
            '<!ENTITY % vocabulary.options',
            '    "decs|icd10|other">',
            ]))

    # Intervention codes
    icodes = map(prep_label_for_xml, InterventionCode.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 13: intervention descriptor attributes -->',
            '<!-- attribute options cannot contain slashes "/" -->',
            '<!ENTITY % interventioncode.options',
            '    "%s">' % '|'.join(icodes), # FIXME: check why labels were defined with
                                            # '-' replacing ' ' on old .mod
            ]))

    # Study statuses
    statuses = map(prep_label_for_xml, RecruitmentStatus.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % requirementstatus.options',
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
    purposes = map(prep_label_for_xml, StudyPurpose.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!-- TRDS 15b: study_design attributes -->',
            '<!ENTITY % purpose.options',
            '    "%s">' % '|'.join(purposes),
            ]))

    # Assignment
    assignments = map(prep_label_for_xml, InterventionAssigment.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % assignment.options',
            '    "%s">' % '|'.join(assignments),
            ]))

    # Masking
    maskings = map(prep_label_for_xml, StudyMasking.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % masking.options',
            '    "%s">' % '|'.join(maskings),
            ]))

    # Allocation
    allocations = map(prep_label_for_xml, StudyAllocation.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % allocation.options',
            '    "%s">' % '|'.join(allocations),
            ]))

    # Phases
    phases = map(prep_label_for_xml, StudyPhase.objects.values_list('label', flat=True))
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
    countries = CountryCode.objects.values_list('label', flat=True)
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
    study_types = map(prep_label_for_xml, StudyType.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % study_type.options',
            '    "%s">' % '|'.join(study_types),
            ]))

    # Institution Types
    institution_types = map(prep_label_for_xml, InstitutionType.objects.values_list('label', flat=True))
    entities.append('\n'.join([
            '<!ENTITY % institution_type.options',
            '    "%s">' % '|'.join(institution_types),
            ]))

    return MOD_TEMPLATE%{
            'generation': datetime.date.today().strftime('%Y-%m-%d'),
            'entities': '\n\n'.join(entities),
            }

