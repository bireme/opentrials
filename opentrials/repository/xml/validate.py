#!/usr/bin/env python

import sys, os
from lxml import etree

cur_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DTD = os.path.join(cur_dir, 'opentrials.dtd')

def validate_xml(filename, dtd=DEFAULT_DTD):
    """
    Validates a XML file according to a given DTD file.
    """
    parser = etree.XMLParser(dtd_validation=False)
    dtd = etree.DTD(dtd)
    tree = etree.parse(filename, parser)
    
    valid = dtd.validate(tree)

    return valid or dtd.error_log.filter_from_errors()

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print '%-16s' % arg,

        try:
            result = validate_xml(arg)
        except etree.XMLSyntaxError, e:
            print 'ERROR: malformed XML: %s' % e
        else:    
            if result is True:
                print 'OK'
            else:
                print 'INVALID'
                print result[0]

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

