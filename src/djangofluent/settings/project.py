"""
Project specific settings
"""
from .defaults import *
from django.utils.translation import ugettext_lazy as _

# Admins receive 500 errors, managers receive 404 errors.
ADMINS = (
    ('Edoburu', 'sysadmin@edoburu.nl'),
)
MANAGERS = ADMINS

SERVER_MAIL = 'sysadmin@edoburu.nl'
DEFAULT_FROM_EMAIL = 'sysadmin@edoburu.nl'
EMAIL_SUBJECT_PREFIX = '[Django][djangofluent] '

# Project language settings
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en'

# Database to use
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',  # or mysql
        'NAME':     'django-fluent.org',
        'USER':     'djangofluent',
        'PASSWORD': 'testtest',
    },
}

SECRET_KEY = '!k95k&wn43_8b5rp*c$+9pzcl=$w9s9o&t##x7os$3p3l%57&w'

# Apps to use
INSTALLED_APPS += (
    # Site design
    'frontend',

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
    'fluent_contents.plugins.sharedcontent',
    'fluent_contents.plugins.rawhtml',
    'fluent_contents.plugins.text',

    # Site parts
    'apps.themeelements',
    'apps.wysiywg_config',

    # Support libs
    'analytical',
    'any_imagefield',
    'any_urlfield',
    'axes',
    'categories_i18n',
    'crispy_forms',
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


MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryLogMiddleware',       # make 'request' available on all logs.
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',  # on 404, report to sentry.
) + MIDDLEWARE_CLASSES + (
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',  # on 404, try redirect fallback
    'fluent_contents.middleware.HttpRedirectRequestMiddleware',        # allow plugin redirects
)

TEMPLATES[0]['OPTIONS']['context_processors'] += (
    'frontend.context_processors.frontend',
)

TEMPLATES[0]['OPTIONS']['loaders'] += (
    'admin_tools.template_loaders.Loader',  # Allow {% extends "appname:template" %}
)

FORMAT_MODULE_PATH = 'djangofluent.settings.locale'  # Consistent date formatting

# Avoid 600 permission for filebrowser uploads.
FILE_UPLOAD_PERMISSIONS = 0o644

IGNORABLE_404_URLS = (
    #re.compile(r'^/favicon.ico$'),
    #re.compile(r'^/wp-login.php$'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': u'%(levelname)s: %(asctime)s %(process)d %(thread)d %(module)s: %(message)s',
        },
        'simple': {
            'format': u'%(levelname)s:\t%(message)s',
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


## -- Third party app settings

ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

AXES_LOGIN_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = 1  # hours
AXES_IP_WHITELIST = INTERNAL_IPS

CRISPY_TEMPLATE_PACK = 'bootstrap3'

COMMENTS_APP = 'fluent_comments'

DJANGO_WYSIWYG_FLAVOR = 'tinymce_advanced'

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.png', '.gif'],
    'Document': ['.pdf', '.doc', '.xls', '.csv', '.docx', '.xlsx'],
    'Video': ['.swf', '.mp4', '.flv', '.f4v', '.mov', '.3gp'],
}
FILEBROWSER_EXCLUDE = ('cache', '_versions', '_admin_thumbnail\.', '_big\.', '_large\.', '_medium\.', '_small\.', '_thumbnail\.')
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

FLUENT_BLOGS_EXTRA_ADMIN_FIELDS = ('intro',)
FLUENT_BLOGS_ENTRY_LINK_STYLE = '/{year}/{month}/{slug}/'
FLUENT_BLOGS_INCLUDE_STATIC_FILES = False  # done in base.html by us.

FLUENT_COMMENTS_MODERATE_AFTER_DAYS = 30
FLUENT_COMMENTS_EXCLUDE_FIELDS = ('url',)
FLUENT_COMMENTS_FIELD_ORDER = ('comment', 'name', 'email')
FLUENT_COMMENTS_MODERATE_AFTER_DAYS = 30

FLUENT_CONTENTS_CACHE_OUTPUT = True

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

PING_CHECKS = (
    'ping.checks.check_database_sessions',
    'ping.checks.check_database_sites',
    #'ping.checks.check_celery', # Fails..
)

TAGGIT_TAGS_FROM_STRING = 'taggit_selectize.utils.parse_tags'
TAGGIT_STRING_FROM_TAGS = 'taggit_selectize.utils.join_tags'

THUMBNAIL_DEBUG = False
THUMBNAIL_FORMAT = 'JPEG'


## -- Site app settings

PACKAGEITEM_INTERNAL_GITHUB_ORG = 'edoburu'
