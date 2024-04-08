"""
Django settings for djangofluent project.
"""
import environ
import os
import re

import raven.exceptions
from django.utils.translation import gettext_lazy as _

import djangofluent

env = environ.Env()

# --- Environment

SITE_ID = 1
DEBUG = env.bool('DJANGO_DEBUG', True)

SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
ROOT_DIR = os.path.dirname(SRC_DIR)

# Paths
MEDIA_ROOT = ROOT_DIR + '/web/media/'
MEDIA_URL = '/media/'        # Must end with /
ROOT_URLCONF = 'djangofluent.urls'

STATIC_ROOT = ROOT_DIR + '/web/static/'
STATIC_URL = '/static/'

# --- Locale settings

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True                   # False for optimizations
USE_L10N = True
USE_TZ = True

# --- Email

ADMINS = (
    ('Edoburu', 'sysadmin@edoburu.nl'),
)
MANAGERS = ADMINS

SERVER_MAIL = 'sysadmin@edoburu.nl'
DEFAULT_FROM_EMAIL = 'sysadmin@edoburu.nl'
EMAIL_SUBJECT_PREFIX = '[Django][djangofluent] '

# --- Security

SECRET_KEY = env.str('DJANGO_SECRET_KEY', '!k95k&wn43_8b5rp*c$+9pzcl=$w9s9o&t##x7os$3p3l%57&w')
SESSION_COOKIE_HTTPONLY = True  # can't read cookie from JavaScript
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', False)

X_FRAME_OPTIONS = 'SAMEORIGIN'  # Prevent iframes. Can be overwritten per view using the @xframe_options_.. decorators

INTERNAL_IPS = ('127.0.0.1',)

IGNORABLE_404_URLS = (
    re.compile(r'^favicon.ico$'),
    # re.compile(r'^/favicon.ico$'),
    # re.compile(r'^/wp-login.php$'),
)

# --- Plugin components

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'compressor',

    # Site parts
    'frontend',
    'djangofluent.apps.themeelements',
    'djangofluent.apps.wysiywg_config',

    # CMS parts
    'fluent_blogs',
    'fluent_blogs.pagetypes.blogpage',
    'fluent_pages',
    'fluent_pages.pagetypes.fluentpage',
    'fluent_pages.pagetypes.flatpage',
    'fluent_pages.pagetypes.redirectnode',
    'fluent_comments',
    'fluent_contents',
    'fluent_contents.plugins.code',
    'fluent_contents.plugins.commentsarea',
    'fluent_contents.plugins.gist',
    'fluent_contents.plugins.oembeditem',
    'fluent_contents.plugins.picture',
    'fluent_contents.plugins.rawhtml',
    'fluent_contents.plugins.sharedcontent',
    'fluent_contents.plugins.text',

    # Support libs
    'analytical',
    'any_imagefield',
    'any_urlfield',
    'axes',
    'categories_i18n',
    'crispy_forms',
    "crispy_bootstrap3",
    'django_comments',
    'django_wysiwyg',
    'django.contrib.redirects',
    'filebrowser',
    'mptt',
    'parler',
    'polymorphic',
    'polymorphic_tree',
    'slug_preview',
    'staff_toolbar',
    'sorl.thumbnail',
    'taggit',
    'taggit_selectize',
    'threadedcomments',
    'tinymce',

    # and enable the admin
    'fluent_dashboard',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

FORMAT_MODULE_PATH = 'djangofluent.settings.locale'  # Consistent date formatting

LOCALE_PATHS = (
    os.path.join(SRC_DIR, 'locale'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Generate cache-busing static file names that can have a far-future expire headers
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = (
    'raven.contrib.django.middleware.SentryMiddleware',  # make 'request' available on all logs.
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',  # on 404, try redirect fallback
    'fluent_contents.middleware.HttpRedirectRequestMiddleware',
    'axes.middleware.AxesMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (),
        'OPTIONS': {
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',  # Allow {% extends "appname:template" %}
            ),
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'frontend.context_processors.frontend',
            ),
        },
    },
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# --- Services

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

CACHES = {
    'default': env.cache(default='dummycache://'),
    'axes': env.cache(default='dummycache://'),
}

DATABASES = {
    'default': env.db(default='postgresql://djangofluent:testtest@127.0.0.1/django-fluent.org'),
}

locals().update(env.email_url(default='smtp://'))

RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', default=''),
}

try:
    GIT_VERSION = raven.fetch_git_sha('..')
    RAVEN_CONFIG['release'] = GIT_VERSION
except raven.exceptions.InvalidGitRepository:
    pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s: %(asctime)s %(process)d %(thread)d %(module)s: %(message)s',
        },
        'simple': {
            'format': '%(levelname)s:\t%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',  # to show queries or not.
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

# --- Third party app settings

ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

AXES_CACHE = 'axes'
AXES_LOGIN_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = 1  # hours
AXES_IP_WHITELIST = INTERNAL_IPS

CRISPY_TEMPLATE_PACK = "bootstrap3"

COMMENTS_APP = 'fluent_comments'

COMPRESS_CSS_HASHING_METHOD = None  # WhiteNoise already hashes files. Use 'content' otherwise for multi-server setups

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
)

COMPRESS_JS_FILTERS = (
    'compressor.filters.jsmin.JSMinFilter',
)

COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', not DEBUG)

DJANGO_WYSIWYG_FLAVOR = 'tinymce_advanced'

FILE_UPLOAD_PERMISSIONS = 0o644  # Avoid 600 permission for filebrowser uploads.

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.png', '.gif'],
    'Document': ['.pdf', '.doc', '.xls', '.csv', '.docx', '.xlsx'],
    'Video': ['.swf', '.mp4', '.flv', '.f4v', '.mov', '.3gp'],
}
FILEBROWSER_EXCLUDE = ('cache', '_versions', r'_admin_thumbnail\.', r'_big\.', r'_large\.', r'_medium\.', r'_small\.', r'_thumbnail\.')
FILEBROWSER_MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # in bytes
FILEBROWSER_STRICT_PIL = True
FILEBROWSER_ADMIN_VERSIONS = [
    'thumbnail',
    #'small',
    #'medium',
    #'big',
    #'large',
]
FILEBROWSER_ADMIN_THUMBNAIL = 'admin_thumbnail'
FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': 'Small', 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium', 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big', 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large', 'width': 680, 'height': '', 'opts': ''},
}
FILEBROWSER_VERSION_QUALITY = 80  # Good enough visually, and for Google Pagespeed

FLUENT_BLOGS_EXTRA_ADMIN_FIELDS = ('intro',)
FLUENT_BLOGS_ENTRY_LINK_STYLE = '/{year}/{month}/{slug}/'
FLUENT_BLOGS_INCLUDE_STATIC_FILES = False  # done in base.html by us.

FLUENT_COMMENTS_EXCLUDE_FIELDS = ('url',)
FLUENT_COMMENTS_FIELD_ORDER = ('comment', 'name', 'email')
FLUENT_COMMENTS_MODERATE_AFTER_DAYS = 30

FLUENT_CONTENTS_CACHE_OUTPUT = True
FLUENT_CONTENTS_CACHE_PLACEHOLDER_OUTPUT = False

FLUENT_DASHBOARD_APP_ICONS = {}
FLUENT_DASHBOARD_DEFAULT_MODULE = 'ModelList'

#FLUENT_OEMBED_SOURCE = 'noembed'

FLUENT_PAGES_DEFAULT_IN_NAVIGATION = True
FLUENT_PAGES_TEMPLATE_DIR = os.path.join(SRC_DIR, 'frontend', 'templates')

FLUENT_TEXT_CLEAN_HTML = True
FLUENT_TEXT_SANITIZE_HTML = True
FLUENT_TEXT_PRE_FILTERS = (
    'fluent_contents.plugins.text.filters.smartypants.smartypants_filter',
)

GOOGLE_ANALYTICS_PROPERTY_ID = env.str('GOOGLE_ANALYTICS_PROPERTY_ID', None)
GOOGLE_ANALYTICS_ANONYMIZE_IP = True  # GDPR

HEALTH_CHECKS = {
    'database': 'django_healthchecks.contrib.check_database',
    'cache': 'django_healthchecks.contrib.check_cache_default',
    'ip': 'django_healthchecks.contrib.check_remote_addr',
    'git_version': 'djangofluent.lib.healthchecks.git_version',
}
HEALTH_CHECKS_ERROR_CODE = 503

IPWARE_META_PRECEDENCE_ORDER = (
    # Avoid IP address spoofing for django-axes. Use wsgi-unproxy instead,
    # which tests against a fixed set of incoming sender addresses.
    'REMOTE_ADDR',
)

TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'

THUMBNAIL_DEBUG = False
THUMBNAIL_FORMAT = 'JPEG'
THUMBNAIL_QUALITY = 80  # default quality for mozjpeg's "cjpeg -optimize" is 75
THUMBNAIL_ALTERNATIVE_RESOLUTIONS = [2]  # Generate 2x images for everything!


# --- Site app settings

PACKAGEITEM_INTERNAL_GITHUB_ORG = 'edoburu'
