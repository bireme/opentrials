#!/usr/bin/env python

import sys, os
from lxml import etree

cur_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DTD = os.path.join(cur_dir, 'opentrials.dtd')
ICTRP_DTD = os.path.join(cur_dir, 'who_ictrp.dtd')

class InvalidOpenTrialsXML(Exception): pass

def validate_xml(filename_or_xmltree, dtd=DEFAULT_DTD):
    """
    Validates a XML file according to a given DTD file.
    """
    parser = etree.XMLParser(dtd_validation=False)
    dtd = etree.DTD(dtd)

    if isinstance(filename_or_xmltree, basestring):
        tree = etree.parse(filename_or_xmltree, parser)
    else:
        tree = filename_or_xmltree
    
    valid = dtd.validate(tree)

    if not valid:
        raise InvalidOpenTrialsXML(dtd.error_log.filter_from_errors())

    return True

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print '%-16s' % arg,

        try:
            result = validate_xml(arg)
        except etree.XMLSyntaxError, e:
            print 'ERROR: malformed XML: %s' % e
        except InvalidOpenTrialsXML, e:
            print 'INVALID'
            print e
        else:    
            print 'OK'

""" # OLD CODE:

parser = etree.XMLParser(dtd_validation=False)

dtd = etree.DTD('opentrials.dtd')
for arg in sys.argv[1:]:
    print '%-16s' % arg,
    try:
        tree = etree.parse(arg, parser)
    except etree.XMLSyntaxError:
        print 'ERROR: malformed XML'
    else:    
        if dtd.validate(tree):
            print 'OK'
        else:
            print 'INVALID'
            print dtd.error_log.filter_from_errors()[0]
"""

