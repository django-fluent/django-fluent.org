"""
Project specific settings
"""
from .defaults import *

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
        'OPTIONS':  {'autocommit': True,},   # Stop that "current transaction is aborted" error
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
    'any_imagefield',
    'any_urlfield',
    'axes',
    'categories',
    'categories.editor',
    'crispy_forms',
    'django.contrib.comments',
    'django_wysiwyg',
    'filebrowser',
    'google_analytics',
    'mptt',
    'parler',
    'polymorphic',
    'polymorphic_tree',
    'staff_toolbar',
    'sorl.thumbnail',
    'taggit',
    'taggit_autosuggest',
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

MIDDLEWARE_CLASSES += (
    'axes.middleware.FailedLoginMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'frontend.context_processors.frontend',
)

FORMAT_MODULE_PATH = 'djangofluent.settings.locale'  # Consistent date formatting

# Avoid 600 permission for filebrowser uploads.
FILE_UPLOAD_PERMISSIONS = 0644

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': u'%(levelname)s: %(asctime)s %(process)d %(thread)d %(module)s: %(message)s',
        },
        'simple': {
            'format': u'%(levelname)s: %(message)s',
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
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',  # to show queries or not.
        },
    }
}

## -- Third party app settings

ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

COMMENTS_APP = 'fluent_comments'

DJANGO_WYSIWYG_FLAVOR = 'tinymce_advanced'
#DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + 'frontend/vendor/tiny_mce/'

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.png', '.gif'],
    'Document': ['.pdf', '.doc', '.xls', '.csv', '.docx', '.xlsx'],
    'Video': ['.swf', '.mp4', '.flv', '.f4v', '.mov', '.3gp'],
}
FILEBROWSER_EXCLUDE = ('cache', '_admin_thumbnail\.', '_big\.', '_large\.', '_medium\.', '_small\.', '_thumbnail\.')
FILEBROWSER_MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # in bytes
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

FLUENT_BLOGS_BASE_TEMPLATE = 'base_blog.html'
FLUENT_BLOGS_ENTRY_LINK_STYLE = '/{year}/{month}/{slug}/'
FLUENT_BLOGS_INCLUDE_STATIC_FILES = False  # done in base.html by us.

FLUENT_CONTENTS_CACHE_OUTPUT = True

FLUENT_COMMENTS_EXCLUDE_FIELDS = ('url',)

FLUENT_DASHBOARD_APP_ICONS = {}
FLUENT_DASHBOARD_DEFAULT_MODULE = 'ModelList'

#FLUENT_OEMBED_SOURCE = 'noembed'

FLUENT_PAGES_BASE_TEMPLATE = 'base_flatpage.html'  # for fluent_pages.pagetypes.flatpage
FLUENT_PAGES_DEFAULT_IN_NAVIGATION = True
FLUENT_PAGES_TEMPLATE_DIR = os.path.join(SRC_DIR, 'frontend', 'templates')

FLUENT_TEXT_CLEAN_HTML = True
FLUENT_TEXT_SANITIZE_HTML = True

THUMBNAIL_DEBUG = False
THUMBNAIL_FORMAT = 'JPEG'


## -- Site app settings

PACKAGEITEM_INTERNAL_GITHUB_ORG = 'edoburu'
