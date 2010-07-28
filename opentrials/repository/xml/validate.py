#!/usr/bin/env python

import sys
from lxml import etree

parser = etree.XMLParser(dtd_validation=False)

dtd = etree.DTD('reclac.dtd')
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
    

