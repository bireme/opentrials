"""
     >>> from models import Item, Attribute
     >>> i = Item()
     >>> i.title = 'The Title'
     >>> i.save()
     >>> k = i.key
     >>> del i
     >>> i = Item.get(k)
     >>> i.title
     'The Title'

"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


