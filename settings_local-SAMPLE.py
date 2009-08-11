DATABASE_ENGINE = 'mysql'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'clinicaltrials' # Or path to database file if using sqlite3.
DATABASE_USER = 'tester'       # Not used with sqlite3.
DATABASE_PASSWORD = 'puffpuff' # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SECRET_KEY = 'rmbg(!8sa@&8o9pnnd@*szm+axos_6r$)r48jc2r$^_8+wz)po'

MIDDLEWARE_CLASSES += (
    # 'debug_middleware.DebugFooter',
)
