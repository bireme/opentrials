#coding: utf-8
import unittest
from django.test.client import Client
from django.utils.simplejson import loads as json_loads

class  TestsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_single_level(self):
        response =  self.client.get('/icd10/get_chapters/')
        self.failUnlessEqual(response.status_code, 200)

        json = json_loads(response.content)
        self.assertEqual(type(json), list, "It should be a list")
        self.assertTrue(len(json) > 0, "The list is not empty ")

        self.assertTrue('fields' in json[0],
                        "All elements in the list is a dict with 'fields' key")
        
        self.assertTrue('description' in json[0]['fields'],
                        "The dict above is also a dict with 'description' key")
        
        # currently only the portuguese is supported
        
#        self.assertTrue('en' in json[0]['fields']['description'],
#                        "The dict must contain a label in the language en")
#        
#        self.assertTrue('es' in json[0]['fields']['description'],
#                        "The dict must contain a label in the language es")
                                      
        self.assertTrue('pt' in json[0]['fields']['description'],
                        "The dict must contain a label in the language pt")

    def test_search(self):
        response =  self.client.get('/icd10/search/pt-br/diarreia')
        self.failUnlessEqual(response.status_code, 200)

        json = json_loads(response.content)
        self.assertEqual(type(json), list, "It should be a list")
        self.assertTrue(len(json) > 0, "The list is not empty ")

        self.assertTrue('fields' in json[0],
                        "All elements in the list is a dict with 'fields' key")

        self.assertTrue('description' in json[0]['fields'],
                        "The dict above is also a dict with 'description' key")

        self.assertTrue('en' in json[0]['fields']['description'],
                        "The dict must contain a label in the language en")
        
        self.assertTrue('es' in json[0]['fields']['description'],
                        "The dict must contain a label in the language es")
                                      
        self.assertTrue('pt' in json[0]['fields']['description'],
                        "The dict must contain a label in the language pt")

        self.assertTrue('A09' in (f['fields']['label'] for f in json ),
                        "At least, A09 code should be found")

if __name__ == '__main__':
    unittest.main()

