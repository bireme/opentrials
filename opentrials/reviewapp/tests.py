"""
---------------------------------------
Testing mandatory languages
---------------------------------------

Mandatory languages are English, the language
of the primary sponsor and the languages of the
recruitment countries limited to EN, PT, ES, FR::

    >>> from reviewapp.models import Submission
    >>> from repository.models import ClinicalTrial, Institution
    >>> from vocabulary.models import CountryCode
    >>> i = Institution()
    >>> i.country = CountryCode.objects.get(label='BR')
    >>>
    >>> ct = ClinicalTrial()
    >>> ct.primary_sponsor = i
    >>> ct.save()
    >>>
    >>> s = Submission()
    >>> s.trial = ct
    >>> sorted(s.get_mandatory_languages())
    [u'en', u'pt']

    >>> ct.recruitment_country.add(CountryCode.objects.get(label='AR'))
    >>> ct.save()
    >>> sorted(s.get_mandatory_languages())
    [u'en', u'es', u'pt']

    >>> ct.recruitment_country.add(CountryCode.objects.get(label='SR'))
    >>> ct.save()
    >>> sorted(s.get_mandatory_languages())
    [u'en', u'es', u'pt']
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


