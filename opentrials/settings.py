# -*- encoding: utf-8 -*-

# OpenTrials: a clinical trials registration system
#
# Copyright (C) 2010 BIREME/PAHO/WHO, ICICT/Fiocruz e
#                    Ministério da Saúde do Brasil
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Luciano Ramalho', 'luciano.ramalho@bireme.org'),
    ('Antonio Ribeiro Alves', 'antonio.alves@bireme.org')
)

MANAGERS = ADMINS

DATABASE_OPTIONS = {"init_command": "SET storage_engine=INNODB"}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

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
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    #'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.scriptprefix.ScriptPrefixMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'middleware.user_locale.UserLocaleMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'flatpages_polyglot.middleware.FlatPagePolyglotMiddleware',
)

ROOT_URLCONF = 'opentrials.urls'
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
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.syndication',
    
    'deleting',
    'vocabulary',
    'repository',
    'reviewapp',
    'tickets',
    'assistance',
    'decsclient',
    'icd10client',
    'diagnostic',
    'polyglot',
    'registration',  # django-registration package
    'flatpages_polyglot',
    'south',
    'fossil',
    'rosetta',

    #'debug_toolbar',
    'compressor',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'context_processors.opentrials.polyglot',
    'context_processors.opentrials.google_analytics',
    'context_processors.opentrials.latest_tweets',
    'context_processors.opentrials.debug',
    'context_processors.opentrials.default_from_email',
    'context_processors.opentrials.opentrials_version',
)

AUTH_PROFILE_MODULE = "reviewapp.UserProfile"

#################################################################
### BEGIN Clinical Trials Repository customization settings
###
### see also settings_local-SAMPLE.py for private customization settings.

# this id must match the record with the correct domain name in the
# django_site table; the initial values for that table are defined
# in opentrials/fixtures/initial_data.json
SITE_ID = 2 # change if necessary to match a record in django_site

SITE_TITLE = u'Registro Brasileiro de Ensaios Clínicos'
SEND_BROKEN_LINK_EMAILS = True
DECS_SERVICE = 'http://decs.bvs.br/cgi-bin/mx/cgi=@vmx/decs'
ICD10_SERVICE = 'http://bases.bireme.br/cgi-bin/mxlindG4.exe/cgi=@cid10/cid10'

TRIAL_ID_PREFIX = 'RBR'
TRIAL_ID_DIGITS = 6

# Notes:
# 1) source: http://www.i18nguy.com/unicode/language-identifiers.html
# 2) the first managed language is considered the default and is
#    also the source language for content translation purposes
MANAGED_LANGUAGES_CHOICES = (
    (u'en', u'English'),
    (u'es', u'Español'),
    (u'pt-br', u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:] # exlude source language
MANAGED_LANGUAGES = [code for code, label in MANAGED_LANGUAGES_CHOICES]
# TODO: implement this as default on new submission forms
#LANGUAGES = MANAGED_LANGUAGES_CHOICES
DEFAULT_SUBMISSION_LANGUAGE = u'en'

# django-registration: for how long the activation link is valid
ACCOUNT_ACTIVATION_DAYS = 7

# django-registration: set to False to suspend new user registrations
REGISTRATION_OPEN = True

ATTACHMENTS_DIR = 'attachments'
SUBMISSIONS_XML_PATH = 'submissions_xml'

# Name of Primary Registry
REG_NAME = 'REBEC'

FIXTURE_DIRS = ('fixtures',)

PAGINATOR_CT_PER_PAGE = 10

TWITTER = 'ensaiosclinicos'
TWITTER_TIMEOUT = 18000 # expires in 5 min

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-coverage', '--with-doctest', '--doctest-tests', '--doctest-extension=txt'] # --doctest-fixtures, --with-profile
#NOSE_PLUGINS = []
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

FORMAT_MODULE_PATH = 'formats'

# Backup directory
BACKUP_DIR = os.path.join(MEDIA_ROOT, 'backup')

INTERNAL_IPS = ('127.0.0.1',)
USE_ETAGS = True

COMPRESS = True
COMPRESS_OUTPUT_DIR = 'compressor-cache'
#COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']
#COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

### END Clinical Trials Repository customization settings
#################################################################

# Deployment settings: there *must* be an unversioned settings_local.include
# file in the current directory. See sample file at settings_local-SAMPLE.include
# FIXME: why not use a simple "try: from settings_local import * except ImportError: pass" ?
execfile(os.path.join(PROJECT_PATH,'settings_local.include'))

#check for write permission in static/attachments, for user's uploads
ATTACHMENTS_PATH = os.path.join(MEDIA_ROOT, ATTACHMENTS_DIR)
if os.path.exists(ATTACHMENTS_PATH):
    if not os.access(ATTACHMENTS_PATH, os.W_OK):
        raise IOError('Attachments folder "%s" must be writeable' %
                                (ATTACHMENTS_PATH))
else:
    raise IOError('Attachments folder "%s" not found' % (ATTACHMENTS_PATH))

OPENTRIALS_VERSION = 'v1.1.0rc1' # this should be the deployed tag number
