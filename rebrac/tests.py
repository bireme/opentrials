"""
---------------------------------------
Testing mandatory languages
---------------------------------------

Mandatory languages are English, the language
of the primary sponsor and the languages of the
recruitment countries limited to EN, PT, ES, FR::

    >>> from rebrac.models import Submission
    >>> from registry.models import ClinicalTrial, Institution, RecruitmentCountry
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
    [u'EN', u'PT']
    
    >>> rc = RecruitmentCountry()
    >>> rc.trial = ct
    >>> rc.country = CountryCode.objects.get(label='AR')
    >>> rc.save()
    >>> sorted(s.get_mandatory_languages())
    [u'EN', u'ES', u'PT']
    
    >>> rc = RecruitmentCountry()
    >>> rc.trial = ct
    >>> rc.country = CountryCode.objects.get(label='SR')
    >>> rc.save()
    >>> sorted(s.get_mandatory_languages())
    [u'EN', u'ES', u'PT']
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


