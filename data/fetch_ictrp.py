#!/usr/bin/env python

import urllib
from zipfile import ZipFile, ZIP_DEFLATED
import time
import os

DUMP_URL = 'http://www.ensaiosclinicos.gov.br/rg/all/xml/ictrp'

base_name = 'rebec-ictrp-{0}'.format(time.strftime('%Y-%m-%d'))

zip_name = base_name+'.zip'

archive = ZipFile(zip_name, 'w', ZIP_DEFLATED)

print 'Saving ICTRP dump from ReBEC ...'

xml_name = base_name+'.xml' 

with open(xml_name, 'wb') as xml_file:
    for line in urllib.urlopen(DUMP_URL):
        xml_file.write(line)

print 'Compressing {0} ==> {1} ...'.format(xml_name, zip_name)

archive.write(xml_name)
archive.close()

print 'Deleting {0} ...'.format(xml_name)
os.remove(xml_name)

print 'Done.'
