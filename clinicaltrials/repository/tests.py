import unittest
from django.test.client import Client

from repository.models import *

#class SecondaryNumbers(TestCase):
#    fixtures = ['first_3_trials.json']
#
#    def setUp(self):
#        title = u'Comparison of Ascorbic Acid and Grape Seed'
#        self.asc_trial = ClinicalTrial.objects.get(
#            public_title__istartswith=title)
#
#    def test_short_title(self):
#        start = u'Effect of Ascorbic Acid'
#        self.assert_(self.asc_trial.short_title().startswith(start))
#
#    def test_secondary_numbers(self):
#        self.assert_(len(self.asc_trial.trialnumber_set.all())==2)
#
#    def test_public_contacts(self):
#        contacts = list(self.asc_trial.public_contacts())
#        self.assert_(len(contacts)==1)
#        self.assert_(contacts[0].firstname==u'Naser')
#
#    def test_scientific_contacts(self):
#        contacts = list(self.asc_trial.scientific_contacts())
#        self.assert_(len(contacts)==1)
#        self.assert_(contacts[0].firstname==u'Naser')

class Step3Test(unittest.TestCase):
    
    def setUp(self):
        self.client = Client()
        self.trial = ClinicalTrial.objects.get(pk=1)

    def test_submit(self):
        self.client.login(username='admin',passowrd='qazwsx')
        response = self.client.post('/rg/step_3/1/',{
            'hc_freetext':'test text to step 3',
            'g-0-vocabulary':'DeCS',
            'g-0-code':'C02',
            'g-0-text':'Virus diseases',
            's-0-vocabulary':'DeCS',
            's-0-code':'C03.752.530',
            's-0-text':'Malaria',
            })
        self.failUnlessEqual(response.status_code, 200)

        print self.client.content



