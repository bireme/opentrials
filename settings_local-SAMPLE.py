DEBUG = True

ADMINS = (
    ('Webmaster Ensaios Clinicos', 'appec@bireme.org'),
)

DATABASE_ENGINE = 'mysql'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'clinicaltrials' # Or path to database file if using sqlite3.
DATABASE_USER = 'tester'       # Not used with sqlite3.
DATABASE_PASSWORD = 'puffpuff' # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SECRET_KEY = 'rmbg(!8sa@&8o9pnnd@*szm+axos_6r$)r48jc2r$^_8+wz)po'

EMAIL_HOST = 'pombo.bireme.br'
EMAIL_PORT = 25 # http://www.iana.org/assignments/port-numbers
### if set, used to authenticate with SMTP
EMAIL_HOST_USER = 'appec@bireme.org'
EMAIL_HOST_PASSWORD = '?????'
EMAIL_USE_TLS = False

SERVER_EMAIL = EMAIL_HOST_USER

if DEBUG:
    MIDDLEWARE_CLASSES += (
        ## external dependency for debug purposes only
        # 'debug_middleware.DebugFooter',
    )

    INSTALLED_APPS += (
        ## external dependency for generating model ER diagrams
        # 'graphviz',
    )

    GRAPHVIZ_DOT_CMD = '/usr/bin/dot'
