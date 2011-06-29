# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest
from django.test.client import Client

class  TestsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_single_level(self):
        response =  self.client.get('/decs/getdescendants/C')
        self.failUnlessEqual(response.status_code, 200)

        json = eval(response.content)
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

    def test_search(self):
        response =  self.client.get('/decs/search/pt-br/sangue')
        self.failUnlessEqual(response.status_code, 200)

        json = eval(response.content)
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

        self.assertTrue('Q50.040.020' in (f['fields']['label'] for f in json ),
                           "At least, the /sangue qualificator should be found")

if __name__ == '__main__':
    unittest.main()

