import re
from lxml.etree import ElementTree

from django.core.management import setup_environ
import settings
setup_environ(settings)

from vocabulary.models import CountryCode, StudyType, StudyPurpose, StudyMasking
from vocabulary.models import InterventionAssigment, StudyAllocation, StudyPhase
from vocabulary.models import RecruitmentStatus

from repository.models import ClinicalTrial, Institution, TrialSecondarySponsor
from repository.models import TrialSupportSource, Contact, SiteContact, PublicContact
from repository.models import ScientificContact, InterventionCode

def post_save_submission(xml_file_path):
    clinical_trial_xpath = {
        'trial_id':'',
        'date_registration':'',
        'scientific_title':'trial_identification/scientific_title',
        'scientific_acronym':'trial_identification/scientific_acronym',
        'public_title':'trial_identification/public_title',
        'acronym':'trial_identification/acronym',
        'hc_freetext':'health_conditions/freetext',
        'i_freetext':'interventions/freetext',
        'inclusion_criteria':'recruitment/inclusion_criteria',
        'gender':'recruitment/gender/@value',
        'agemin_value':'recruitment/agemin',
        'agemin_unit':'recruitment/agemin/@unit',
        'agemax_value':'recruitment/agemax',
        'agemax_unit':'recruitment/agemax/@unit',
        'exclusion_criteria':'recruitment/exclusion_criteria',
        'study_design':'study_type/study_design',
        'expanded_access_program':'study_type/study_design/@expanded_access_program',
        'number_of_arms':'study_type/study_design/@number_of_arms',
        'date_enrollment_anticipated':'recruitment/date_enrolment_anticipated',
        'date_enrollment_actual':'recruitment/date_enrolment_actual',
        'target_sample_size':'recruitment/target_size',
        'created':'',
        'updated':'',
        'exported':'',
        'status':'',
        'staff_note':''
    }

    contact_types_map = {
        'public_contact':PublicContact,
        'scientific_contact':ScientificContact,
        'site_contact':SiteContact
    }

    study_design_map = {
        'allocation': StudyAllocation,
        'intervention_assignment':InterventionAssigment,
        'masking': StudyMasking,
        'purpose':  StudyPurpose
    }

    xml = open(xml_file_path)
    tree = ElementTree()
    root = tree.parse(xml)

    ct = ClinicalTrial()
    ct.save()

    # Non-relational Fields from Clinical Trial
    for field,xpath in clinical_trial_xpath.items():
        if xpath != '':
            resultEl = root.xpath(xpath)
            if len(resultEl) > 0:
                if hasattr(resultEl[0],'text'):
                    setattr(ct, field, resultEl[0].text)
                else:
                    setattr(ct, field, resultEl[0])

    # Add Sponsors
    for sponsorNode in root.xpath('sponsors_and_support/*'):
        sponsor = Institution()
        sponsor.name = sponsorNode.find('name').text
        sponsor.address = sponsorNode.find('address').text
        sponsor.country = CountryCode.objects.get(label=sponsorNode.attrib['country_code'])
        sponsor.save()
        if sponsorNode.tag == 'primary_sponsor':
            ct.primary_sponsor = sponsor
        elif sponsorNode.tag == 'secondary_sponsor':
            TrialSecondarySponsor.objects.create(trial=ct,institution=sponsor)
        elif sponsorNode.tag == 'source_support':
            TrialSupportSource.objects.create(trial=ct,institution=sponsor)

    # Add Contacts
    contactList = {}
    for personNode in root.xpath('contacts/person'):
        contact = Contact()

        for attr in ['firstname','middlename','lastname','email','address','city','zip','telephone']:
            value = personNode.find(attr)
            if value is not None:
                setattr(contact, attr, value.text)
        contact.country = CountryCode.objects.get(label=sponsorNode.attrib['country_code'])
        contact.save()
        contactList[ personNode.attrib['pid'] ] = contact

    # Assign PublicContact, ScientificContact and SiteContact to the trial
    for cType,model in contact_types_map.items():
        for typeNode in root.xpath('contacts/'+cType):
            pattern = re.compile('p[0-9]+')
            for person in pattern.findall(typeNode.attrib['persons']):
                model.objects.create(trial=ct,contact=contactList[person])

    # Interventions
    for icodeNode in root.xpath('interventions/i_code'):
        i_code = InterventionCode.objects.get(label=icodeNode.attrib['value'])
        if isinstance(i_code,InterventionCode):
            ct.i_code.add(i_code)

    # Recruitment Country
    for rcountryNode in root.xpath('recruitment/recruitment_country'):
        ccode = CountryCode.objects.get(label=rcountryNode.attrib['value'])
        if isinstance(ccode,CountryCode):
            ct.recruitment_country.add(ccode)

    # StudyType
    study_type_node = StudyType.objects.get(label=root.attrib['type'])
    if study_type_node is not None:
        ct.study_type = study_type_node

    study_design_node = root.find('study_type/study_design')
    if study_design_node is not None:
        for attr,model in study_design_map.items():
            setattr(ct, attr, model.objects.get(label=study_design_node.attrib[attr]))

    study_phase_node = root.find('study_type/phase')
    if study_phase_node is not None:
        ct.phase = StudyPhase.objects.get(label=study_phase_node.attrib['value'])

    recruitment_status = RecruitmentStatus.objects.get(label = root.find('recruitment').attrib['study_status'])
    if recruitment_status is not None:
        ct.status = recruitment_status
