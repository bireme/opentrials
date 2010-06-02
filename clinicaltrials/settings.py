# -*- encoding: utf-8 -*-
# Django settings for clinicaltrials project.

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Luciano Ramalho', 'luciano.ramalho@bireme.org'),
    ('Fabio Montefuscolo', 'fabio.montefuscolo@bireme.org'),
)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Brasilia'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '*06=j&&^n71^a&%%3rs%7lla+^(n^v1w@@dp_rxvi#&(xo7meq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.user_locale.UserLocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.scriptprefix.ScriptPrefixMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

)

ROOT_URLCONF = 'clinicaltrials.urls'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'repository',
    'vocabulary',
    'reviewapp',
    'tickets',
    'assistance',
    'decsclient',
    'diagnostic',
    'polyglot',
    'rosetta',
    'registration',  # django-registration package
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
)

AUTH_PROFILE_MODULE = "reviewapp.UserProfile"

#################################################################
### BEGIN Clinical Trials Repository customization settings
###
### see also settings_local-SAMPLE.py for private customization settings.

# this id must match the record with the correct domain name in the
# django_site table; the initial values for that table are defined
# in clinicaltrials/fixture/initial_data.json
SITE_ID = 2 # change if necessary to match a record in django_site

SITE_TITLE = u'Registro Brasileiro de Ensaios Clínicos'
SEND_BROKEN_LINK_EMAILS = True
DECS_SERVICE = 'http://decs.bvs.br/cgi-bin/mx/cgi=@vmx/decs'

# Notes:
# 1) source: http://www.i18nguy.com/unicode/language-identifiers.html
# 2) the first managed language is considered the default and is
#    also the source language for content translation purposes
MANAGED_LANGUAGES = (
    (u'en-US',u'English'),
    (u'es-ES',u'Español'),
    #(u'fr-FR',u'Français'),
    (u'pt-BR',u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES[1:] # exlude source language
CHECKED_LANGUAGES = [code for code, label in MANAGED_LANGUAGES]

# django-registration: for how long the activation link is valid
ACCOUNT_ACTIVATION_DAYS = 7

# django-registration: set to False to suspend new user registrations
REGISTRATION_OPEN = True

ATTACHMENTS_PATH = os.path.join(MEDIA_ROOT, 'attachments')
SUBMISSIONS_XML_PATH = os.path.join(MEDIA_ROOT, 'submissions_xml')

FIXTURE_DIRS = ('fixtures',)

PAGINATOR_CT_PER_PAGE = 10

### END Clinical Trials Repository customization settings
#################################################################

# Deployment settings: there *must* be an unversioned settings_local.py
# file in the current directory. See sample file at settings_local-SAMPLE.py
execfile(os.path.join(PROJECT_PATH,'settings_local.py'))
