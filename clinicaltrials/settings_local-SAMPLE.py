DEBUG = False

ADMINS = (
    ('Webmaster Ensaios Clinicos', 'appec@bireme.org'),
)

DATABASES = {
    'default' : {
        'ENGINE':'mysql',
        'NAME':'clinicaltrials',
        'USER':'tester',
        'PASSWORD':'puffpuff',
    }
}

SECRET_KEY = 'rmbg(!8sa@&8o9pnnd@*szm+axos_6r$)r48jc2r$^_8+wz)po'

EMAIL_HOST = 'pombo.bireme.br'
EMAIL_PORT = 25 # http://www.iana.org/assignments/port-numbers
### if set, used to authenticate with SMTP
EMAIL_HOST_USER = 'appec@bireme.org'
EMAIL_HOST_PASSWORD = '?????'
EMAIL_USE_TLS = False

SERVER_EMAIL = EMAIL_HOST_USER

if DEBUG:
    DEBUG_PROPAGATE_EXCEPTIONS = True
    MIDDLEWARE_CLASSES += (
        ## external dependency for debug purposes only
        # 'debug_middleware.DebugFooter',
    )

    INSTALLED_APPS += (
        ## external dependency for generating model ER diagrams
        # 'graphviz',
    )

    GRAPHVIZ_DOT_CMD = '/usr/bin/dot'
