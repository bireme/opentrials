#!/usr/bin/env python

'''
Load translations for country names by country code
'''

############# spells to setup the django machinery
import sys, os
here = os.path.abspath(os.path.split(__file__)[0])
above = os.path.split(here)[0]
sys.path.append(above)

from django.core.management import setup_environ
import settings
setup_environ(settings)
############# /spells

from vocabulary.models import CountryCode, VocabularyTranslation

language = 'pt'
filename = 'countries_%s.txt' % language

unknown = []
for lin in (lin.strip() for lin in open(filename)):
    if not lin or lin.startswith('#'):
        continue
    cc, name = lin.split(None,1)
    try:
        country = CountryCode.objects.get(label=cc)
    except CountryCode.DoesNotExist:
        unknown.append(cc)
    print '%s %-40s %-40s' % (cc, country, name)
    trans = VocabularyTranslation(language=language, label=cc, description=name)
    country.translations.add(trans)
if unknown:
    print '*** unknown:', unknown