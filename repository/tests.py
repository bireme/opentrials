from django.test import TestCase
from repository.models import *

class SecondaryNumbers(TestCase):
    fixtures = ['first_3_trials.json']

    def setUp(self):
        title = u'Comparison of Ascorbic Acid and Grape Seed'
        self.asc_trial = ClinicalTrial.objects.get(
            public_title__istartswith=title)

    def test_short_title(self):
        start = u'Effect of Ascorbic Acid'
        self.assert_(self.asc_trial.short_title().startswith(start))

    def test_secondary_numbers(self):
        self.assert_(len(self.asc_trial.trialnumber_set.all())==2)

    def test_public_contacts(self):
        contacts = list(self.asc_trial.public_contacts())
        self.assert_(len(contacts)==1)
        self.assert_(contacts[0].firstname==u'Naser')

    def test_scientific_contacts(self):
        contacts = list(self.asc_trial.scientific_contacts())
        self.assert_(len(contacts)==1)
        self.assert_(contacts[0].firstname==u'Naser')
