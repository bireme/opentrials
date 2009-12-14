import os, sys
sys.path.append('/home/aplicacoes-bvs/rebrac-alfa/clinicaltrials')
sys.path.append('/home/aplicacoes-bvs/rebrac-alfa')
os.environ['DJANGO_SETTINGS_MODULE'] = 'clinicaltrials.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

