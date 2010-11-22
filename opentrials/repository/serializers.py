import datetime
from django.utils import simplejson
from django.db.models import Model
from django.contrib.auth.models import User
from fossil.fields import FossilProxy

def serialize_trial(trial, as_string=True, attrs_to_ignore=None):
    """
    Serialize a given ClinicalTrial and its dependencies in once trunk.

    This function is used for djang-fossil to fossilize this object and
    make possible to generate other formats (i.e: opentrials.dtd) and
    keep revisions of a trial in denormalized mode in database.

    Returns a text JSON to be used anywhere.

    The argument 'as_string' sets to return serialized as String. If False,
    it will return a dict.

    XXX Questions to solve:

        * Should us serialize empty fields as None or ignore them?
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

        if isinstance(value, datetime.datetime):
            value = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.date):
            value = value.strftime('%Y-%m-%d')
        elif isinstance(value, User):
            value = serialize_user(value, as_string=False)
        elif isinstance(value, Model):
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

        # TODO FIXME XXX
        json[field.name] = [item.serialize_for_fossil(as_string=False) for item in objects.all()]

    json['__unicode__'] = unicode(trial)
    json['__model__'] = trial.__class__.__name__
    json['pk'] = trial.pk

    if as_string:
        json = simplejson.dumps(json)

    return json

def deserialize_trial(data, persistent=False):
    """
    Gets a JSON text data and converts to an instance of ClinicalTrial model class.
    TODO: confirm if this must be a proxy class
    """
    json = simplejson.loads(data)

    if persistent:
        pass # TODO
    else:
        return FossilClinicalTrial(data)

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

class FossilClinicalTrial(FossilProxy):
    """
    This class has the same interface of a ClinicalTrial object, but its behaviour
    is to be a proxy of deserialized fossilized version of a trial.

    The instance of this class is not persistent.
    """
    
    def __getattr__(self, name):
        value = super(FossilClinicalTrial, self).__getattr__(name)

        if isinstance(value, basestring):
            if name in ('date_registration','created','updated','exported'):
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

        return value

