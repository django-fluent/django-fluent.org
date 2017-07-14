from djangofluent.settings.defaults import *

# All environment settings can be overwritten with `docker run -e`

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=('django-fluent.org', 'localhost',))

DEBUG = env.bool('DJANGO_DEBUG', default=False)

if not DEBUG:
    # Production!
    COMPRESS_ENABLED = True
    FLUENT_CONTENTS_CACHE_OUTPUT = True
    FLUENT_CONTENTS_CACHE_PLACEHOLDER_OUTPUT = True

    # https only site, see http://ponycheckup.com/
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', True)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)

    # SSL settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
