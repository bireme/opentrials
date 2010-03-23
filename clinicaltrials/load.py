import re
from lxml.etree import ElementTree

from django.core.management import setup_environ
import settings
setup_environ(settings)

from vocabulary.models import CountryCode
from repository.models import ClinicalTrial, Institution, TrialSecondarySponsor
from repository.models import TrialSupportSource, Contact, SiteContact, PublicContact
from repository.models import ScientificContact, InterventionCode

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

contact_types = {
    'public_contact':PublicContact,
    'scientific_contact':ScientificContact,
    'site_contact':SiteContact
}


xml = open('repository/xml/sample_1b.xml')
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
                ct.__setattr__(field,resultEl[0].text)
            else:
                ct.__setattr__(field,resultEl[0])


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
            contact.__setattr__(attr,value.text)
    contact.country = CountryCode.objects.get(label=sponsorNode.attrib['country_code'])
    contact.save()
    contactList[ personNode.attrib['pid'] ] = contact

# Assign PublicContact, ScientificContact and SiteContact to the trial
for cType,model in contact_types.items():
    for typeNode in root.xpath('contacts/'+cType):
        pattern = re.compile('p[0-9]+')
        for person in pattern.findall(typeNode.attrib['persons']):
            model.objects.create(trial=ct,contact=contactList[person])

#Interventions
for icodeNode in root.xpath('interventions/i_code'):
    i_code = InterventionCode.objects.get(label=icodeNode.attrib['value'])
    if isinstance(i_code,InterventionCode):
        ct.i_code.add(i_code)
