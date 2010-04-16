#!/usr/bin/env python

import twill
from twill import commands as tc
from twill.shell import TwillCommandLoop
from django.test import TestCase
from django.core.servers.basehttp import AdminMediaHandler
from django.core.handlers.wsgi import WSGIHandler
from StringIO import StringIO

# Functions you'll need:

def twill_setup():
    app = AdminMediaHandler(WSGIHandler())
    twill.add_wsgi_intercept("127.0.0.1", 8080, lambda: app)

def twill_teardown():
    twill.remove_wsgi_intercept('127.0.0.1', 8080)

def make_twill_url(url):
    # modify this
    return url.replace("http://ubuntu/", 
                       "http://127.0.0.1:8080/")

def twill_quiet():
    # suppress normal output of twill.. You don't want to 
    # call this if you want an interactive session
    twill.set_output(StringIO())

# Example tests. (This code has not been tested, as it 
# would require a website to exist, but very similar 
# code is working on my machine)

class AccessTest(TestCase):
    def setUp(self):
        twill_setup()

    def tearDown(self):
        twill_teardown()

    def test1(self):
        url = "http://www.yourwebsite.com/signup/"
        twill_quiet()
        tc.go('ubuntu')
        tc.find('Registro Brasileiro')
        tc.follow('register')
        tc.url()
        # Fill in the form
        tc.fv('1', 'username', 'test123')
        tc.fv('1', 'email', 'test1@lab.tmp.br')
        tc.submit()
        tc.find('click the activation link')

    def unfinished_test(self):
        # Some complicated set up here, perhaps
        # url = "http://www.yourwebsite.com/prefs/"
        # tc.go(make_twill_url(url))

        # The following will launch into an interactive twill session
        # cmd = TwillCommandLoop()
        # cmd.cmdloop()


