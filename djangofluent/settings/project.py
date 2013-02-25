"""
Project specific settings
"""
from .defaults import *

# Database to use
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'django-fluent.org',
        'USER':     'djangofluent',
        'PASSWORD': 'testtest',
    },
}

SECRET_KEY = '!k95k&amp;wn43_8b5rp*c$+9pzcl=$w9s9o&amp;t##x7os$3p3l%57&amp;w'

# Apps to use
INSTALLED_APPS += (
    # Site parts
    'frontend',

    # CMS
    'fluent_pages',
    'fluent_pages.pagetypes.fluentpage',
    'fluent_contents',
    'fluent_contents.plugins.text',

    # Support libs
    'crispy_forms',
    'django_wysiwyg',
    'filebrowser',
    'google_analytics',
    'mptt',
    'polymorphic',
    'polymorphic_tree',
    'sorl.thumbnail',
    'tinymce',

    # and enable the admin
    'fluent_dashboard',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'frontend.context_processors.site',
)

FORMAT_MODULE_PATH = 'djangofluent.settings.locale'  # Consistent date formatting

# App specific settings
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'  # for filebrowser

ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'

DJANGO_WYSIWYG_FLAVOR = 'tinymce_advanced'
#DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + 'frontend/vendor/tiny_mce/'

FILEBROWSER_DIRECTORY = ''
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.png', '.gif'],
    'Document': ['.pdf', '.doc', '.xls', '.csv', '.docx', '.xlsx'],
    'Video': ['.swf', '.mp4', '.flv', '.f4v', '.mov', '.3gp'],
}
FILEBROWSER_MAX_UPLOAD_SIZE = '104857600'  # in bytes
FILEBROWSER_SAVE_FULL_URL = False

FLUENT_DASHBOARD_APP_ICONS = {}
FLUENT_DASHBOARD_DEFAULT_MODULE = 'ModelList'

FLUENT_PAGES_TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'frontend', 'templates')
