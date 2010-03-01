#!/usr/bin/env python

'''

    >>> from lxml import etree
    >>> parser = etree.XMLParser(dtd_validation=True)
    >>> tree = etree.parse('sample_0.xml', parser)
    Traceback (most recent call last):
      ...
    XMLSyntaxError: Opening and ending tag mismatch: study_type...
    >>> tree = etree.parse('sample_2.xml', parser)
    >>> trial = tree.getroot()
    >>> trial.attrib['type']
    'interventional'
    >>> for e in trial: print e.tag
    public_title
    study_design
    >>> title = trial.find('public_title')
    >>> title.text
    'Comparison of Vitamin C...
    >>> title.attrib['lang']
    'en'
    >>> tree = etree.parse('sample_4.xml', parser)
    >>> title = tree.find('public_title')
    >>> 'vitamina C' in title.text
    True
    >>> title.attrib['lang']
    'pt-br'
    
'''

import doctest
doctest.testmod(optionflags=doctest.ELLIPSIS)
