import os, sys
sys.path.append('/home/aplicacoes-bvs/ensaiosclinicos/clinicaltrials')
sys.path.append('/home/aplicacoes-bvs/ensaiosclinicos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'clinicaltrials.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

