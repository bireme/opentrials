#!/usr/bin/env python

import sys
import urllib2

import httplib

SERVER = 'www.ensaiosclinicos.gov.br' 
PATH = '/rg/%s/'

with open(sys.argv[1], 'r') as id_file:
    for i, trial_id in list(enumerate(id_file)):
        trial_id = trial_id.strip()
        print '*'*50, i+1, trial_id
        cnx = httplib.HTTPConnection(SERVER)
        cnx.request('GET', PATH % trial_id)
        res = cnx.getresponse()
        print res.status, res.reason
        cnx.close()

