from .. import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = True

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

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

ALLOWED_HOSTS = (
    '.django-fluent.org',
)

CACHES['default']['KEY_PREFIX'] = 'djangofluent.beta'

#INSTALLED_APPS += ('gunicorn',)
