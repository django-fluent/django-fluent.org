from .. import *

DEBUG = False
COMPRESS_ENABLED = True

# https only site
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Example:
#
#DATABASES = {
#    'default': {
#        'ENGINE':   'django.db.backends.postgresql_psycopg2',
#        'NAME':     'beta.django-fluent.org',
#        'USER':     'djangofluent',
#        'PASSWORD': 'mY0H8XTwo20gxGY2',
#    },
#}

INSTALLED_APPS += (
)

TEMPLATES[0]['OPTIONS']['loaders'] = (
    ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
)

ALLOWED_HOSTS = (
    '.django-fluent.org',
)

CACHES['default']['KEY_PREFIX'] = 'djangofluent.beta'
