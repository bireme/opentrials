try:
  from lxml import etree
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
        except ImportError:
          raise Exception("Failed to import lxml/ElementTree from any known place")

import re
from datetime import datetime
from django.db.models.fields import NOT_PROVIDED, CharField, TextField
from repository.models import ClinicalTrial, Institution, PublicContact, ScientificContact
from repository.models import SiteContact, TrialNumber, TrialSecondarySponsor, TrialSupportSource
from repository.models import Outcome, Descriptor, Contact
from vocabulary.models import StudyType, StudyPurpose, InterventionAssigment, StudyMasking
from vocabulary.models import StudyAllocation, StudyPhase, RecruitmentStatus, CountryCode
from vocabulary.models import InterventionCode
from repository.xml import OPENTRIALS_XML_VERSION
from validate import validate_xml, ICTRP_DTD

UPDATE_IF_EXISTS = 'u'
REPLACE_IF_EXISTS = 'r'
SKIP_IF_EXISTS = 's'

GENDERS = {'both':'-', 'male':'M', 'female':'F'}
AGE_UNITS = {'null':'-', 'years':'Y', 'months':'M', 'weeks':'W', 'days':'D', 'hours':'H'}
EXP_AGE_ICTRP = re.compile('^(\d+)(-|Y|M|W|D|H)?$')

class OpenTrialsXMLImport(object):
    def __init__(self, creator=None):
        self.creator = creator

    # OPENTRIALS XML

    def parse_opentrials(self, filename_or_xmltree):
        """
        Validates a given file and parses it without to persist on database. Collected
        trials are just saved in the attribute '_parsed_trials' to be imported after.

        For WHO OpenTrials XML format.
        """
        # Validates using DTD
        validation = validate_xml(filename_or_xmltree)

        if validation is not True:
            raise Exception(validation)

        self._parsed_trials = []
        
        # Loads XML file
        if isinstance(filename_or_xmltree, basestring):
            fp = file(filename_or_xmltree)
            tree = etree.parse(fp)
        else:
            tree = filename_or_xmltree
            fp = None

        trials = tree.getroot()
        trials_attrs = dict(trials.items())

        for trial in trials.iterchildren():
            # Collects the list of trials, as dictionaries
            fields = self.collect_trial_fields_opentrials(trial)

            # Loads the trial from database and clear it or just create a new instance in memory
            try:
                ct = ClinicalTrial.objects.get(trial_id=fields['trial_id'])
            except ClinicalTrial.DoesNotExist:
                ct = None

            self._parsed_trials.append((fields, ct))

        if fp:
            fp.close()

        return self._parsed_trials

    def import_opentrials(self, filename_or_xmltree, if_exists=UPDATE_IF_EXISTS):
        """
        Uses lxml to load a file in OpenTrials XML format and load it into database.
        """

        self.parse_opentrials(filename_or_xmltree)

        return self.import_parsed(if_exists)

    def collect_trial_fields_opentrials(self, node):
        fields = {}
        translations = []

        # Fields: created, date_registration, status, updated
        fields.update(dict(node.items()))

        # Collect fields
        for block in node.iterchildren():
            if block.tag == 'trial_identification':
                for field in block.iterchildren():
                    if field.tag in ('trial_id', 'utrn', 'reg_name', 'public_title', 'acronym',
                                     'acronym_expansion', 'scientific_title', 'scientific_acronym',
                                     'scientific_acronym_expansion'):
                        fields[field.tag] = field.text
            elif block.tag == 'sponsors_and_support':
                for field in block.iterchildren():
                    if field.tag == 'primary_sponsor':
                        fields[field.tag] = self.get_institution(field)
                    elif field.tag == 'secondary_sponsor':
                        fields.setdefault('secondary_sponsors', [])
                        fields['secondary_sponsors'].append(self.get_institution(field))
                    elif field.tag == 'source_support':
                        fields.setdefault('source_support', [])
                        fields['source_support'].append(self.get_institution(field))
            elif block.tag == 'health_conditions':
                for field in block.iterchildren():
                    if field.tag == 'hc_code':
                        fields.setdefault('hc_codes', [])
                        fields['hc_codes'].append(self.get_hc_or_ic(field))
                    elif field.tag == 'keyword':
                        fields.setdefault('hc_keywords', [])
                        fields['hc_keywords'].append(self.get_hc_or_ic(field))
                    elif field.tag == 'freetext':
                        fields['hc_freetext'] = field.text
            elif block.tag == 'interventions':
                for field in block.iterchildren():
                    if field.tag == 'i_code':
                        fields.setdefault('i_codes', [])
                        fields['i_codes'].append(self.get_i_code(field))
                    elif field.tag == 'keyword':
                        fields.setdefault('i_keywords', [])
                        fields['i_keywords'].append(self.get_hc_or_ic(field))
                    elif field.tag == 'freetext':
                        fields['i_freetext'] = field.text
            elif block.tag == 'recruitment':
                fields['recruitment_status'] = dict(block.items())['status']

                for field in block.iterchildren():
                    if field.tag == 'recruitment_country':
                        fields.setdefault('recruitment_country', [])
                        fields['recruitment_country'].append({'label': dict(field.items())['value']})
                    elif field.tag in ('inclusion_criteria','exclusion_criteria'):
                        fields[field.tag] = field.text
                    elif field.tag in ('gender','target_size'):
                        fields[field.tag] = dict(field.items())['value']
                    elif field.tag in ('agemin','agemax'):
                        attrs = dict(field.items())
                        fields[field.tag+'_value'] = attrs['value']
                        fields[field.tag+'_unit'] = attrs['unit']
                    elif field.tag == 'date_enrolment_anticipated':
                        attrs = dict(field.items())
                        fields['enrollment_start_planned'] = attrs['start']
                        fields['enrollment_end_planned'] = attrs['end']
                    elif field.tag == 'date_enrolment_actual':
                        attrs = dict(field.items())
                        fields['enrollment_start_actual'] = attrs['start']
                        fields['enrollment_end_actual'] = attrs['end']
            elif block.tag == 'study':
                # expanded_access_program, number_of_arms
                fields.update(dict(block.items()))

                for field in block.iterchildren():
                    if field.tag == 'study_design':
                        fields[field.tag] = field.text
                    elif field.tag == 'type':
                        fields['study_type'] = dict(field.items())['value']
                    elif field.tag in ('phase', 'purpose', 'intervention_assignment', 'masking', 'allocation'):
                        fields[field.tag] = dict(field.items())['value']
            elif block.tag == 'outcomes':
                for field in block.iterchildren():
                    if field.tag == 'primary_outcome':
                        fields.setdefault('primary_outcomes', [])
                        fields['primary_outcomes'].append(self.get_outcome(field))
                    elif field.tag == 'secondary_outcome':
                        fields.setdefault('secondary_outcomes', [])
                        fields['secondary_outcomes'].append(self.get_outcome(field))
            elif block.tag == 'contacts':
                for field in block.iterchildren():
                    if field.tag == 'person':
                        fields.setdefault('persons', [])
                        fields['persons'].append(self.get_person(field))
                    elif field.tag == 'public_contact':
                        fields.setdefault('public_contact', [])
                        fields['public_contact'].append({'pid': dict(field.items())['person']})
                    elif field.tag == 'scientific_contact':
                        fields.setdefault('scientific_contact', [])
                        fields['scientific_contact'].append({'pid': dict(field.items())['person']})
                    elif field.tag == 'site_contact':
                        fields.setdefault('site_contact', [])
                        fields['site_contact'].append({'pid': dict(field.items())['person']})
            elif block.tag == 'secondary_ids':
                for sid in block.iterchildren():
                    fields.setdefault('secondary_ids', [])
                    sec_id = {}
                    for field in sid.iterchildren():
                        sec_id[field.tag] = field.text
                    fields['secondary_ids'].append(sec_id)
            elif block.tag == 'references':
                for field in block.iterchildren():
                    if field.tag == 'link':
                        fields.setdefault('urls', [])
                        fields['urls'].append(dict(field.items())['url'])
            elif block.tag == 'staff_note':
                fields['staff_note'] = field.text
            elif block.tag == 'translation':
                fields.setdefault('translations', [])
                trans = {}
                for field in block.iterchildren():
                    trans[field.tag] = field.text
                fields['translations'].append(trans)

        return fields

    # WHO ICTRP

    def parse_ictrp(self, filename_or_xmltree):
        """
        Validates a given file and parses it without to persist on database. Collected
        trials are just saved in the attribute '_parsed_trials' to be imported after.

        For WHO ICTRP format.
        """
        # Validates using DTD
        validation = validate_xml(filename_or_xmltree, dtd=ICTRP_DTD)

        if validation is not True:
            raise Exception(validation)

        self._parsed_trials = []
        
        # Loads XML file
        if isinstance(filename_or_xmltree, basestring):
            fp = file(filename_or_xmltree)
            tree = etree.parse(fp)
        else:
            tree = filename_or_xmltree
            fp = None

        trials = tree.getroot()
        trials_attrs = dict(trials.items())

        for trial in trials.iterchildren():
            # Collects the list of trials, as dictionaries
            fields = self.collect_trial_fields_ictrp(trial)

            # Loads the trial from database and clear it or just create a new instance in memory
            try:
                ct = ClinicalTrial.objects.get(trial_id=fields['trial_id'])
            except ClinicalTrial.DoesNotExist:
                ct = None

            self._parsed_trials.append((fields, ct))

        if fp:
            fp.close()

        return self._parsed_trials

    def import_ictrp(self, filename_or_xmltree, if_exists=UPDATE_IF_EXISTS):
        """
        Uses lxml to load a file in OpenTrials XML format and load it into database.
        """

        self.parse_ictrp(filename_or_xmltree)

        return self.import_parsed(if_exists)

    def collect_trial_fields_ictrp(self, node):
        fields = {}
        translations = []

        # Fields: created, date_registration, status, updated
        fields.update(dict(node.items()))

        # Collect fields
        for block in node.iterchildren():
            if block.tag == 'main':
                for field in block.iterchildren():
                    if field.tag in ('trial_id', 'utrn', 'reg_name', 'date_registration',
                                     'public_title', 'acronym', 'scientific_title', 'scientific_acronym',
                                     'date_enrolment', 'type_enrolment', 'target_size', 'recruitment_status',
                                     'url', 'study_type', 'study_design', 'phase', 'hc_freetext', 'i_freetext'):
                        fields[field.tag] = field.text
                    elif field.tag == 'primary_sponsor':
                        fields[field.tag] = {'name': field.text}

                if fields['type_enrolment'] == 'actual':
                    fields['enrollment_start_actual'] = fields['date_enrolment']
                    #fields['enrollment_end_actual']
                    fields.pop('type_enrolment'); fields.pop('date_enrolment')
                else:
                    fields['enrollment_start_planned'] = fields['date_enrolment']
                    #fields['enrollment_end_planned']
                    fields.pop('type_enrolment'); fields.pop('date_enrolment')
            elif block.tag == 'contacts':
                fields.setdefault('persons', [])

                for field in block.iterchildren():
                    contact = self.get_contact_ictrp(field)
                    fields['persons'].append(contact)

                    if contact['type'] == 'public':
                        fields.setdefault('public_contact', [])
                        fields['public_contact'].append({
                            'firstname': contact['firstname'],
                            'middlename': contact['middlename'],
                            'lastname': contact['lastname'],
                            })
                    elif contact['type'] == 'scientific':
                        fields.setdefault('scientific_contact', [])
                        fields['scientific_contact'].append({
                            'firstname': contact['firstname'],
                            'middlename': contact['middlename'],
                            'lastname': contact['lastname'],
                            })
            elif block.tag == 'countries':
                fields.setdefault('recruitment_country', [])
                for item in block.iterchildren():
                    fields['recruitment_country'].append({'description': item.text})
            elif block.tag == 'criteria':
                for item in block.iterchildren():
                    if item.tag in ('inclusion_criteria','exclusion_criteria'):
                        fields[field.tag] = field.text
                    elif item.tag == 'gender':
                        fields[field.tag] = {'F':'female', 'M':'male'}.get(field.text.upper(), 'both')
                    elif item.tag in ('agemin','agemax'):
                        m = EXP_AGE_ICTRP.match(field.text)
                        if m:
                            fields[field.tag+'_value'] = m.groups(1)
                            fields[field.tag+'_unit'] = m.groups(2) or '-'
            elif block.tag == 'health_condition_code':
                fields.setdefault('hc_codes', [])
                for item in block.iterchildren():
                    fields['hc_codes'].append({'code': item.text})
            elif block.tag == 'health_condition_keyword':
                fields.setdefault('hc_keywords', [])
                for item in block.iterchildren():
                    fields['hc_keywords'].append({'code': item.text})
            elif block.tag == 'intervention_code':
                fields.setdefault('i_codes', [])
                for item in block.iterchildren():
                    fields['i_codes'].append({'value': item.text})
            elif block.tag == 'intervention_keyword':
                fields.setdefault('i_keywords', [])
                for item in block.iterchildren():
                    fields['i_keywords'].append({'code': item.text})
            elif block.tag == 'primary_outcome':
                fields.setdefault('primary_outcomes', [])
                for item in block.iterchildren():
                    fields['primary_outcomes'].append({'value': field.text})
            elif block.tag == 'secondary_outcome':
                fields.setdefault('secondary_outcomes', [])
                for item in block.iterchildren():
                    fields['secondary_outcomes'].append({'value': field.text})
            elif block.tag == 'secondary_sponsor':
                fields.setdefault('secondary_sponsors', [])
                for item in block.iterchildren():
                    fields['secondary_sponsors'].append({'name': item.text})
            elif block.tag == 'secondary_ids':
                fields.setdefault('secondary_ids', [])
                for item in block.iterchildren():
                    fields['secondary_ids'].append({'sec_id': item.text})
            elif block.tag == 'source_support':
                fields.setdefault('source_support', [])
                for item in block.iterchildren():
                    fields['source_support'].append({'name': item})

        return fields

    def get_contact_ictrp(self, node):
        ret = {}

        for field in node.iterchildren():
            if field.tag == 'affiliation':
                ret[field.tag] = {'name': field.text}
            elif field.tag == 'country1':
                ret['country_code'] = {'description': field.text}
            else:
                ret[field.tag] = field.text

        return ret

    # ALL FORMATS

    def import_parsed(self, if_exists=UPDATE_IF_EXISTS):
        """
        Imports from parsed trials, stored in the attribute '_parsed_trials'. They
        should be collected using the method 'parse_opentrials'.

        Case "if_exists" ==

        - UPDATE_IF_EXISTS: will keep the trials exactly as they are, just updating their fields.
                            This means that existing child objects will keep as they are, just updating.
        - REPLACE_IF_EXISTS: will empty the current trial and fill its fields again with imported field values.
                             This means that existing child objects will be deleted to have only the imported ones.
        - SKIP_IF_EXISTS: will not import anything for existing trials
        """

        if not hasattr(self, '_parsed_trials'):
            raise Exception(_("To import parsed trials it's necessary to call method 'parse_opentrials' before."))

        imported_trials = []
        
        for fields, ct in self._parsed_trials:
            # Loads the trial from database and clear it or just create a new instance in memory
            if not ct:
                try:
                    ct = ClinicalTrial.objects.get(trial_id=fields['trial_id'])
                except ClinicalTrial.DoesNotExist:
                    ct = None

            if ct:
                if if_exists == SKIP_IF_EXISTS:
                    continue

                elif if_exists == REPLACE_IF_EXISTS:
                    self.clear_fields(ct)
            else:
                ct = ClinicalTrial(trial_id=fields['trial_id'])

            # Sets the field values and clean them
            self.set_trial_fields(ct, fields)

            # Children objects
            self.set_trial_children(ct, fields)

            # TODO: call validation

            # Sets the status as the last thing to make a consistent fossil
            ct.status = ct.new_status
            ct.save()

            imported_trials.append(ct)

        return imported_trials

    def get_default(self, field):
        if isinstance(field.default, NOT_PROVIDED) or field.default == NOT_PROVIDED:
            if isinstance(field, (CharField, TextField)):
                return ''
            else:
                return None
        elif callable(field.default):
            return field.default()
        else:
            return field.default

    def date_from(self, datestr):
        try:
            return datetime.strptime(datestr, '%Y-%m-%d').date()
        except ValueError:
            return datetime.strptime(datestr, '%d/%m/%Y').date()

    def set_trial_fields(self, ct, fields):
        # Char fields
        ct.public_title = fields.get('public_title', None) or ct.public_title
        ct.utrn_number = fields.get('utrn_number', None) or ct.utrn_number
        #ct.reg_name = fields.get('reg_name', None) or ct.reg_name # Maybe should create a new field?
        ct.acronym = fields.get('acronym', None) or ct.acronym
        ct.acronym_expansion = fields.get('acronym_expansion', None) or ct.acronym_expansion
        ct.scientific_title = fields.get('scientific_title', None) or ct.scientific_title
        ct.scientific_acronym = fields.get('scientific_acronym', None) or ct.scientific_acronym
        ct.scientific_acronym_expansion = fields.get('scientific_acronym_expansion', None) or ct.scientific_acronym_expansion
        ct.staff_note = fields.get('staff_note', None) or ct.staff_note
        ct.study_design = fields.get('study_design', None) or ct.study_design
        ct.hc_freetext = fields.get('hc_freetext', None) or ct.hc_freetext
        ct.i_freetext = fields.get('i_freetext', None) or ct.i_freetext
        ct.inclusion_criteria = fields.get('inclusion_criteria', None) or ct.inclusion_criteria
        ct.exclusion_criteria = fields.get('exclusion_criteria', None) or ct.exclusion_criteria
        ct.enrollment_start_planned = fields.get('enrollment_start_planned', None) or ct.enrollment_start_planned
        ct.enrollment_start_actual = fields.get('enrollment_start_actual', None) or ct.enrollment_start_actual
        ct.enrollment_end_planned = fields.get('enrollment_end_planned', None) or ct.enrollment_end_planned
        ct.enrollment_end_actual = fields.get('enrollment_end_actual', None) or ct.enrollment_end_actual
        ct.language = fields.get('language', None) or ct.language
        ct.new_status = fields.get('status', None) or ct.status # Temporary to be saved only in the end of all

        # Integer fields
        ct.agemin_value = fields.get('agemin_value', None) or ct.agemin_value
        ct.agemax_value = fields.get('agemax_value', None) or ct.agemax_value
        ct.number_of_arms = fields.get('number_of_arms', None) or ct.number_of_arms
        ct.target_sample_size = fields.get('target_size', None) or ct.target_sample_size

        # Boolean fields
        if fields.get('expanded_access_program', None):
            ct.expanded_access_program = fields['expanded_access_program'] == 'yes'

        # Date fiels
        if fields.get('updated', None):
            ct.updated = self.date_from(fields['updated'])
        if fields.get('created', None):
            ct.created = self.date_from(fields['created'])
        if fields.get('exported', None):
            ct.exported = self.date_from(fields['exported'])
        if fields.get('date_registration', None):
            ct.date_registration = self.date_from(fields['date_registration'])

        # Flag fields
        ct.gender = GENDERS[fields.get('gender', 'both')]
        ct.agemin_unit = AGE_UNITS[fields.get('agemin_unit', 'null')]
        ct.agemax_unit = AGE_UNITS[fields.get('agemax_unit', 'null')]
        
        # Foreign keys
        if fields.get('primary_sponsor', None):
            ct.primary_sponsor = self.get_instituion_from_db(fields['primary_sponsor'])
        if fields.get('study_type', None):
            ct.study_type, new = StudyType.objects.get_or_create(label=self.prep_label(fields['study_type']))
        if fields.get('purpose', None):
            ct.purpose, new = StudyPurpose.objects.get_or_create(label=self.prep_label(fields['purpose']))
        if fields.get('intervention_assignment', None):
            ct.intervention_assignment, new = InterventionAssigment.objects.get_or_create(label=self.prep_label(fields['intervention_assignment']))
        if fields.get('masking', None):
            ct.masking, new = StudyMasking.objects.get_or_create(label=self.prep_label(fields['masking']))
        if fields.get('allocation', None):
            ct.allocation, new = StudyAllocation.objects.get_or_create(label=self.prep_label(fields['allocation']))
        if fields.get('phase', None):
            ct.phase, new = StudyPhase.objects.get_or_create(label=self.prep_label(fields['phase']))
        if fields.get('recruitment_status', None):
            ct.recruitment_status, new = RecruitmentStatus.objects.get_or_create(label=self.prep_label(fields['recruitment_status']))

        ct.save()

    def set_trial_children(self, ct, fields):
        for country in fields.get('recruitment_country', []):
            if country.get('label', None):
                country_obj, new = CountryCode.objects.get_or_create(
                        label=country['label'],
                        defaults={'description': country.get('description', '')},
                        )
            else:
                country_obj = CountryCode.objects.get(description=country['description'])
            ct.recruitment_country.add(country_obj)

        for person in fields.get('persons', []):
            try:
                if person.get('pid', None):
                    contact = Contact.objects.get(pk=person['pid'])
                else:
                    contact = Contact.objects.get(
                            firstname=person['firstname'],
                            middlename=person['middlename'],
                            lastname=person['lastname'],
                            )
            except Contact.DoesNotExist:
                contact = Contact(creator=self.creator)
                if person.get('pid', None):
                    contact.pk = person['pid']

            contact.firstname = person.get('firstname', contact.firstname)
            contact.middlename = person.get('middlename', contact.middlename)
            contact.lastname = person.get('lastname', contact.lastname)
            contact.address = person.get('address', contact.address)
            contact.city = person.get('city', contact.city)
            if person.get('country_code', None):
                if person['country_code'].get('label', None):
                    contact.country = CountryCode.objects.get(label=person['country_code']['label'])
                else:
                    contact.country = CountryCode.objects.get(description=person['country_code']['description'])
            contact.zip = person.get('zip', contact.zip)
            contact.telephone = person.get('telephone', contact.telephone)
            contact.email = person.get('email', contact.email)
            if person.get('affiliation', None):
                contact.affiliation = self.get_instituion_from_db(person['affiliation'])

            contact.save()

        for item in fields.get('public_contact', []):
            if item.get('pid', None):
                contact = Contact.objects.get(pk=item['pid'])
            else:
                contact = Contact.objects.get(
                        firstname=item['firstname'],
                        middlename=item['middlename'],
                        lastname=item['lastname'],
                        )
            PublicContact.objects.get_or_create(trial=ct, contact=contact)

        for item in fields.get('scientific_contact', []):
            if item.get('pid', None):
                contact = Contact.objects.get(pk=item['pid'])
            else:
                contact = Contact.objects.get(
                        firstname=item['firstname'],
                        middlename=item['middlename'],
                        lastname=item['lastname'],
                        )
            ScientificContact.objects.get_or_create(trial=ct, contact=contact)

        for item in fields.get('site_contact', []):
            contact = Contact.objects.get(pk=item)
            SiteContact.objects.get_or_create(trial=ct, contact=contact)

        for item in fields.get('secondary_ids', []):
            TrialNumber.objects.get_or_create(
                    trial=ct,
                    issuing_authority=item.get('issuing_authority', ''),
                    id_number=item['sec_id'],
                    )

        for item in fields.get('secondary_sponsor', []):
            inst = self.get_instituion_from_db(item)
            TrialSecondarySponsor.objects.get_or_create(trial=ct, institution=inst)

        for item in fields.get('secondary_sponsor', []):
            inst = self.get_instituion_from_db(item)
            TrialSupportSource.objects.get_or_create(trial=ct, institution=inst)

        for item in fields.get('primary_outcomes', []):
            outcome, new = Outcome.objects.get_or_create(trial=ct, interest='primary', description=item['value'])
            for trans in item.get('translations', []):
                outcome.translations.get_or_create(description=trans['description'], language=trans['language'])

        for item in fields.get('secondary_outcomes', []):
            outcome, new = Outcome.objects.get_or_create(trial=ct, interest='secondary', description=item['value'])
            for trans in item.get('translations', []):
                outcome.translations.get_or_create(description=trans['description'], language=trans['language'])

        for item in fields.get('hc_codes', []):
            descriptor, new = Descriptor.objects.get_or_create(
                    trial=ct,
                    aspect='HealthCondition',
                    level='general',
                    vocabulary=item.get('vocabulary', 'DeCS'), # FIXME
                    code=item['code'],
                    defaults={
                        'version': item.get('version', ''),
                        'text': item.get('value', ''),
                        }
                    )
            for trans in item.get('translations', []):
                trans_obj = descriptor.translations.get_translation_for_object(trans['lang'], descriptor, create_if_not_exist=True)
                trans_obj.text=trans['value']
                trans_obj.save()

        for item in fields.get('hc_keywords', []):
            descriptor, new = Descriptor.objects.get_or_create(
                    trial=ct,
                    aspect='HealthCondition',
                    level='specific',
                    vocabulary=item.get('vocabulary', 'DeCS'), # FIXME
                    code=item['code'],
                    defaults={
                        'version': item.get('version', ''),
                        'text': item.get('value', ''),
                        }
                    )
            for trans in item.get('translations', []):
                trans_obj = descriptor.translations.get_translation_for_object(trans['lang'], descriptor, create_if_not_exist=True)
                trans_obj.text=trans['value']
                trans_obj.save()

        for item in fields.get('i_codes', []):
            i_code, new = InterventionCode.objects.get_or_create(label=item['value'])
            ct.i_code.add(i_code)

        for item in fields.get('i_keywords', []):
            descriptor, new = Descriptor.objects.get_or_create(
                    trial=ct,
                    aspect='Intervention',
                    level='specific',
                    vocabulary=item.get('vocabulary', 'DeCS'), # FIXME
                    code=item['code'],
                    defaults={
                        'version': item.get('version', ''),
                        'text': item.get('value', ''),
                        }
                    )
            for trans in item.get('translations', []):
                trans_obj = descriptor.translations.get_translation_for_object(trans['lang'], descriptor, create_if_not_exist=True)
                trans_obj.text=trans['value']
                trans_obj.save()

    def get_institution(self, node):
        ret = dict(node.items())

        for field in node.iterchildren():
            if field.tag in ('name','address'):
                ret[field.tag] = field.text

        return ret

    def get_hc_or_ic(self, node):
        ret = {}
        ret.update(dict(node.items()))

        for field in node.iterchildren():
            if field.tag == 'text':
                ret['value'] = field.text
            elif field.tag == 'text_translation':
                trans = dict(field.items())
                trans['value'] = field.text

                ret.setdefault('translations', [])
                ret['translations'].append(trans)

        return ret

    def get_i_code(self, node):
        return dict(node.items())

    def get_person(self, node):
        ret = {}
        ret.update(dict(node.items()))

        if isinstance(ret.get('country_code', None), basestring):
            ret['country_code'] = {'label': ret['country_code']}

        for field in node.iterchildren():
            if field.tag == 'affiliation':
                ret[field.tag] = self.get_institution(field)
            else:
                ret[field.tag] = field.text

        return ret

    def get_outcome(self, node):
        ret = {}
        ret.update(dict(node.items()))
        ret['translations'] = []

        for field in node.iterchildren():
            if field.tag == 'outcome_translation':
                ret['translations'].append(dict(field.items()))

        return ret

    def clear_fields(self, ct):
        # Update fields to default values
        for field in ClinicalTrial._meta.fields:
            if field.name in ('trial_id','id'):
                continue

            setattr(ct, field.name, self.get_default(field))

        # Remove children
        ct.trialnumber_set.all().delete()
        ct.outcome_set.all().delete()
        ct.trialsecondarysponsor_set.all().delete()
        ct.trialsupportsource_set.all().delete()
        ct.public_contact.all().delete() # pay attention to this - to see what is it deleting
        ct.scientific_contact.all().delete() # pay attention to this - to see what is it deleting
        ct.site_contact.all().delete() # pay attention to this - to see what is it deleting
        ct.descriptor_set.all().delete()
        ct.translations.all().delete()

    def get_instituion_from_db(self, fields):
        if fields.get('country_code', None):
            country = CountryCode.objects.get(label=fields['country_code'])
        else:
            country = CountryCode.objects.all()[0] # FIXME TODO

        inst, new = Institution.objects.get_or_create(
                name=fields['name'],
                country=country,
                address=fields.get('address', ''),
                defaults={'creator': self.creator},
                )
        return inst

    def prep_label(self, label):
        """Because labels replace white spaces for underlines, we must make the contrary
        here to make possible to find them."""
        return label.replace('_', ' ')

