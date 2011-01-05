import datetime

from django.utils import simplejson
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from fossil.fields import FossilProxy, DictKeyAttribute
from polyglot.models import lang_format
from utilities import safe_truncate

def serialize_trial(trial, as_string=True, attrs_to_ignore=None):
    """
    Serialize a given ClinicalTrial and its dependencies in once trunk.

    This function is used for djang-fossil to fossilize this object and
    make possible to generate other formats (i.e: opentrials.dtd) and
    keep revisions of a trial in denormalized mode in database.

    Returns a text JSON to be used anywhere.

    The argument 'as_string' sets to return serialized as String. If False,
    it will return a dict.
    """
    attrs_to_ignore = attrs_to_ignore or []

    json = {}

    # Common fields
    for field in trial._meta.fields:
        if field.name in attrs_to_ignore:
            continue

        try:
            value = getattr(trial, field.name)
        except AttributeError:
            continue
        except ObjectDoesNotExist:
            value = None

        if isinstance(value, datetime.datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        elif isinstance(value, User):
            value = serialize_user(value, as_string=False)
        elif isinstance(value, models.Model):
            value = value.serialize_for_fossil(as_string=False)
        
        json[field.name] = value

    # Many to many fields
    for field in trial._meta.many_to_many:
        if field.name in attrs_to_ignore:
            continue

        try:
            objects = getattr(trial, field.name).all()
        except AttributeError:
            continue

        json[field.name] = [item.serialize_for_fossil(as_string=False) for item in objects.all()]

    # Other attributes
    if hasattr(trial, 'secondary_sponsors'):
        json['secondary_sponsors'] = [item.serialize_for_fossil(as_string=False) for item in trial.secondary_sponsors()]
    if hasattr(trial, 'hc_code'):
        json['hc_code'] = [item.serialize_for_fossil(as_string=False) for item in trial.hc_code()]
    if hasattr(trial, 'hc_keyword'):
        json['hc_keyword'] = [item.serialize_for_fossil(as_string=False) for item in trial.hc_keyword()]
    if hasattr(trial, 'intervention_keyword'):
        json['intervention_keyword'] = [item.serialize_for_fossil(as_string=False) for item in trial.intervention_keyword()]
    if hasattr(trial, 'primary_outcomes'):
        json['primary_outcomes'] = [item.serialize_for_fossil(as_string=False) for item in trial.primary_outcomes()]
    if hasattr(trial, 'secondary_outcomes'):
        json['secondary_outcomes'] = [item.serialize_for_fossil(as_string=False) for item in trial.secondary_outcomes()]
    if hasattr(trial, 'trial_number'):
        json['trial_number'] = [item.serialize_for_fossil(as_string=False) for item in trial.trial_number()]
    if hasattr(trial, 'support_sources'):
        json['support_sources'] = [item.serialize_for_fossil(as_string=False) for item in trial.support_sources()]
    if hasattr(trial, 'acronym_display'):
        json['acronym_display'] = trial.acronym_display()
    if hasattr(trial, 'scientific_acronym_display'):
        json['scientific_acronym_display'] = trial.scientific_acronym_display()
    if hasattr(trial, 'enrollment_start_planned'):
        date = trial.enrollment_start_actual or trial.enrollment_start_planned
        if date:
            date = date.split('-')
            date.reverse()
            json['date_enrollment_start'] = '/'.join(date)

    # Meta or auxiliar attributes
    json['__unicode__'] = unicode(trial)
    json['__model__'] = trial.__class__.__name__
    json['pk'] = trial.pk

    if as_string:
        json = simplejson.dumps(json)

    return json

def deserialize_trial(data, persistent=False, persistency_class=None, commit=True):
    """
    Gets a JSON text data and converts to an instance of ClinicalTrial model class.
    TODO: confirm if this must be a proxy class
    """
    if isinstance(data, basestring):
        json = simplejson.loads(data)
    elif isinstance(data, dict):
        json = data
    else:
        raise Exception('Invalid trial serialized data.')

    if not persistent:
        return FossilClinicalTrial(data)

    else:
        if persistency_class is None:
            raise Exception('Persistent deserialization of a trial must inform the persistency class.')

        from repository.models import ClinicalTrialTranslation, PublicContact, ScientificContact
        from vocabulary.models import StudyType, StudyPurpose, InterventionAssigment
        from vocabulary.models import StudyMasking, StudyAllocation, StudyPhase
        from vocabulary.models import RecruitmentStatus, InterventionCode, CountryCode

        obj_fossil = DictKeyAttribute(json)

        trial = persistency_class()

        # Simple fields
        for field in persistency_class._meta.fields:
            if field.name in ('id','trial_id','status'):
                continue

            try:
                value = getattr(obj_fossil, field.name)
            except AttributeError:
                continue

            if isinstance(field, (models.CharField, models.TextField, models.IntegerField,
                models.PositiveIntegerField, models.DateTimeField, models.DateField,
                models.NullBooleanField, models.BooleanField)):
                setattr(trial, field.name, value)

            elif isinstance(field, models.ForeignKey) and value is not None:
                if field.name == 'primary_sponsor':
                    trial.primary_sponsor = deserialize_institution(value, True)
                elif field.name == 'study_type':
                    trial.study_type = deserialize_vocabulary(value, True, StudyType)
                elif field.name == 'purpose':
                    trial.purpose = deserialize_vocabulary(value, True, StudyPurpose)
                elif field.name == 'intervention_assignment':
                    trial.intervention_assignment = deserialize_vocabulary(value, True, InterventionAssigment)
                elif field.name == 'masking':
                    trial.masking = deserialize_vocabulary(value, True, StudyMasking)
                elif field.name == 'allocation':
                    trial.allocation = deserialize_vocabulary(value, True, StudyAllocation)
                elif field.name == 'phase':
                    trial.phase = deserialize_vocabulary(value, True, StudyPhase)
                elif field.name == 'recruitment_status':
                    trial.recruitment_status = deserialize_vocabulary(value, True, RecruitmentStatus)

        if not commit:
            return trial

        trial.save()

        # Many to many fields
        for contact_fossil in obj_fossil.public_contact:
            contact = deserialize_contact(contact_fossil, True)

            PublicContact.objects.create(trial=trial, contact=contact)

        for contact_fossil in obj_fossil.scientific_contact:
            contact = deserialize_contact(contact_fossil, True)

            ScientificContact.objects.create(trial=trial, contact=contact)

        for icode_fossil in obj_fossil.i_code:
            icode = deserialize_vocabulary(icode_fossil, True, InterventionCode)

            trial.i_code.add(icode)

        for country_fossil in obj_fossil.recruitment_country:
            country = deserialize_vocabulary(country_fossil, True, CountryCode)

            trial.recruitment_country.add(country)

        # Translations
        for trans_fossil in obj_fossil.translations:
            trans = deserialize_trial(trans_fossil, True, ClinicalTrialTranslation, False)
            trans.content_object = trial
            trans.save()

        # Saves trial again to force fields validation
        trial.save()

        return trial

def serialize_institution(institution, as_string=True):
    """
    Serializes a given institution object to JSON
    """
    json = {
        'pk': institution.pk,
        'name': institution.name,
        'address': institution.address,
        'country': institution.country.serialize_for_fossil(as_string=False),
        'creator': serialize_user(institution.creator, as_string=False),
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def deserialize_institution(data, persistent=False):
    """
    Transforms data (as JSON string or a dict) to an institution
    """
    if not data:
        return None

    if not persistent:
        pass # TODO if necessary

    else:
        from repository.models import Institution
        from vocabulary.models import CountryCode, InstitutionType

        if isinstance(data, basestring):
            data = DictKeyAttribute(simplejson.loads(data))
        elif isinstance(data, dict):
            data = DictKeyAttribute(data)

        try:
            institution = Institution.objects.get(pk=data.pk)
        except Institution.DoesNotExist:
            institution = Institution()
            institution.id = data.pk
            institution.name = data.name
            institution.address = data.address
            institution.country = deserialize_vocabulary(data.country, True, CountryCode)
            institution.creator = deserialize_user(data.creator, True)
            institution.i_type = deserialize_vocabulary(data.i_type, True, InstitutionType)
            institution.save()

        return institution

def deserialize_vocabulary(data, persistent=False, persistency_class=None):
    """
    Transforms data (as JSON string or a dict) to a vocabulary instance of
    the given class
    """
    if not data:
        return None

    if not persistent:
        pass # TODO if necessary

    else:
        if persistency_class is None:
            raise Exception('Persistent deserialization of a vocabulary object must inform the persistency class.')

        if isinstance(data, basestring):
            data = DictKeyAttribute(simplejson.loads(data))
        elif isinstance(data, dict):
            data = DictKeyAttribute(data)

        try:
            obj = persistency_class.objects.get(label=data.label)
        except persistency_class.DoesNotExist:
            obj = persistency_class()
            obj.label = data.label
            obj.description = data.description
            obj.save()

        return obj

def serialize_contact(contact, as_string=True):
    """
    Serializes a given contact object to JSON
    """
    json = {
        'pk': contact.pk,
        'firstname': contact.firstname,
        'middlename': contact.middlename,
        'lastname': contact.lastname,
        'email': contact.email,
        'affiliation': serialize_institution(contact.affiliation, as_string=False) if contact.affiliation else None,
        'address': contact.address,
        'city': contact.city,
        'country': contact.country.serialize_for_fossil(as_string=False) if contact.country else None,
        'zip': contact.zip,
        'telephone': contact.telephone,
        'creator': serialize_user(contact.creator, as_string=False) if contact.creator else None,
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def deserialize_contact(data, persistent=False):
    """
    Transforms data (as JSON string or a dict) to a contact object
    """
    if not data:
        return None

    if not persistent:
        pass # TODO if necessary

    else:
        from repository.models import Contact
        from vocabulary.models import CountryCode

        if isinstance(data, basestring):
            data = DictKeyAttribute(simplejson.loads(data))
        elif isinstance(data, dict):
            data = DictKeyAttribute(data)

        try:
            obj = Contact.objects.get(pk=data.pk)
        except Contact.DoesNotExist:
            obj = Contact()
            obj.id = data.pk
            obj.firstname = data.firstname
            obj.middlename = data.middlename
            obj.lastname = data.lastname
            obj.email = data.email
            obj.affiliation = deserialize_institution(data.affiliation, True)
            obj.address = data.address
            obj.city = data.city
            obj.country = deserialize_vocabulary(data.country, True, CountryCode)
            obj.zip = data.zip
            obj.telephone = data.telephone
            obj.creator = deserialize_user(data.creator, True)
            obj.save()

        return obj

def serialize_user(user, as_string=True):
    """
    Serializes a given user object to JSON
    """
    json = {
        'username': user.username,
        'email': user.email,
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def deserialize_user(data, persistent=False):
    """
    Transforms data (as JSON string or a dict) to a Django user
    """
    if not data:
        return None

    if not persistent:
        pass # TODO if necessary

    else:
        if isinstance(data, basestring):
            data = DictKeyAttribute(simplejson.loads(data))
        elif isinstance(data, dict):
            data = DictKeyAttribute(data)

        try:
            obj = User.objects.get(username=data.username)
        except User.DoesNotExist:
            obj = User()
            obj.username = data.username
            obj.email = data.email
            obj.save()

        return obj

def serialize_trialnumber(trialnumber, as_string=True):
    """
    Serializes a given trial number object to JSON
    """
    json = {
            'issuing_authority': trialnumber.issuing_authority,
            'id_number': trialnumber.id_number,
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def serialize_trialsupportsource(source, as_string=True):
    """
    Serializes a given trial support source object to JSON
    """
    json = {
            'institution': serialize_institution(source.institution, as_string=False),
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def serialize_trialsecondarysponsor(sponsor, as_string=True):
    """
    Serializes a given trial number object to JSON
    """
    json = {
            'institution': serialize_institution(sponsor.institution, as_string=False),
        }

    if as_string:
        json = simplejson.dumps(json)

    return json

def serialize_outcome(outcome, as_string=True):
    """
    Serializes a given trial outcome object to JSON
    """
    json = {
            'description': outcome.description,
        }

    if hasattr(outcome, 'interest'):
        json['interest'] = outcome.interest

    if hasattr(outcome, 'language'):
        json['language'] = outcome.language

    if hasattr(outcome, 'translations'):
        json['translations'] = [serialize_outcome(trans, as_string=False)
                for trans in outcome.translations.all()]

    if as_string:
        json = simplejson.dumps(json)

    return json

def serialize_descriptor(descriptor, as_string=True):
    """
    Serializes a given trial descriptor object to JSON
    """
    json = {
            'text': descriptor.text,
        }

    if hasattr(descriptor, 'aspect'):
        json['aspect'] = descriptor.aspect

    if hasattr(descriptor, 'vocabulary'):
        json['vocabulary'] = descriptor.vocabulary

    if hasattr(descriptor, 'version'):
        json['version'] = descriptor.version

    if hasattr(descriptor, 'level'):
        json['level'] = descriptor.level

    if hasattr(descriptor, 'code'):
        json['code'] = descriptor.code

    if hasattr(descriptor, 'language'):
        json['language'] = descriptor.language

    if hasattr(descriptor, 'translations'):
        json['translations'] = [serialize_descriptor(trans, as_string=False)
                for trans in descriptor.translations.all()]

    if as_string:
        json = simplejson.dumps(json)

    return json

class FossilClinicalTrial(FossilProxy):
    """
    This class has the same interface of a ClinicalTrial object, but its behaviour
    is to be a proxy of deserialized fossilized version of a trial.

    The instance of this class is not persistent.
    """
    _language = None
    _translations = None

    def _load_translations(self):
        if self._translations is None:
            self._translations = dict([(lang_format(t.get('language', '').lower()), t)
                for t in self.object_fossil.translations])
    
    def __getattr__(self, name):
        value = super(FossilClinicalTrial, self).__getattr__(name)

        if name in ('date_registration','created','updated','exported'):
            if isinstance(value, basestring):
                try:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    value = datetime.datetime.strptime(value, '%Y-%m-%d')

        elif isinstance(value, dict) and value.get('translations', None):
            try:
                value = [t for t in value['translations'] if t.get('language', '').lower() == self._language.lower()][0]
            except IndexError:
                pass

        elif self._language:
            self._load_translations()

            try:
                value_trans = self._translations[lang_format(self._language)][name]
                if value_trans:
                    value = value_trans
            except KeyError:
                pass

        return value

    def main_title(self):
        if self.public_title:
            return self.public_title
        else:
            return self.scientific_title

    def rec_status(self):
        self._load_translations()

        try:
            value = self._translations[lang_format(self._language)]['recruitment_status']
        except KeyError:
            value = self.recruitment_status

        # FIXME This should be serialized with right translation, so the following code
        # would be unnecessary
        if value:
            from vocabulary.models import RecruitmentStatus
            try:
                rec_status = RecruitmentStatus.objects.get(label=value['label'])
                trans = rec_status.translations.get(language=lang_format(self._language))
                return trans.label
            except ObjectDoesNotExist:
                return value['label']

        return value

    def short_title(self):
        return safe_truncate(self.main_title(), 120)

    @property
    def recruitment_country(self):
        countries = super(FossilClinicalTrial, self).__getattr__('recruitment_country')

        def get_trans(item):
            try:
                return [t for t in item['translations'] if t.get('language', '').lower() == self._language.lower()][0]
            except IndexError:
                return item

        return map(get_trans, countries)

    @property
    def i_code(self):
        codes = super(FossilClinicalTrial, self).__getattr__('i_code')

        def get_trans(item):
            try:
                return [t for t in item['translations'] if t.get('language', '').lower() == self._language.lower()][0]
            except IndexError:
                return item

        return map(get_trans, codes)

    @property
    def public_contact(self):
        contacts = super(FossilClinicalTrial, self).__getattr__('public_contact')

        contacts = [FossilContact(contact, language=self._language) for contact in contacts]

        return contacts

    @property
    def scientific_contact(self):
        contacts = super(FossilClinicalTrial, self).__getattr__('scientific_contact')

        contacts = [FossilContact(contact, language=self._language) for contact in contacts]

        return contacts

class FossilContact(FossilProxy):
    _language = None

    def __init__(self, contact, language):
        contact['__model__'] = 'Contact'

        super(FossilContact, self).__init__(contact)

        self._language = language

    @property
    def country(self):
        country = super(FossilContact, self).__getattr__('country')

        try:
            return [t for t in country['translations'] if t.get('language', '').lower() == self._language.lower()][0]
        except IndexError:
            return country

