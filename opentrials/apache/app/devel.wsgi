import os, sys
sys.path.append('/home/luciano/prj/ct/svn/trunk/opentrials')
sys.path.append('/home/luciano/prj/ct/svn/trunk')
os.environ['DJANGO_SETTINGS_MODULE'] = 'opentrials.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

