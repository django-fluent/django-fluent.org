from os import path

import admin_tools.urls
import django.contrib.sitemaps.views
import django.views.defaults
import django.views.static
import django_healthchecks.urls
import fluent_comments.urls
import fluent_pages.urls
import taggit_selectize.urls
import tinymce.urls

from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from filebrowser.sites import site as fb_site
from fluent_blogs.sitemaps import EntrySitemap, CategoryArchiveSitemap, AuthorArchiveSitemap, TagArchiveSitemap
from fluent_pages.sitemaps import PageSitemap
from fluent_pages.views import RobotsTxtView
from frontend.views import Http500View, serve_web_file

sitemaps = {
    'pages': PageSitemap,
    'blog_entries': EntrySitemap,
    'blog_categories': CategoryArchiveSitemap,
    'blog_authors': AuthorArchiveSitemap,
    'blog_tags': TagArchiveSitemap,
}

urlpatterns = [
    # Django admin
    path('admin/filebrowser/', fb_site.urls),
    path('admin/', admin.site.urls),
    path('admin/util/tags/', include(taggit_selectize.urls)),
    path('admin/util/tinymce/', include(tinymce.urls)),
    path('admin/util/tools/', include(admin_tools.urls)),

    # Test pages
    path('500test/', view=Http500View.as_view()),
    path('400/', django.views.defaults.bad_request, kwargs={'exception': None}),
    path('403/', django.views.defaults.permission_denied, kwargs={'exception': None}),
    path('404/', django.views.defaults.page_not_found, kwargs={'exception': None}),
    path('500/', django.views.defaults.server_error),

    # SEO API's
    re_path(r'^sitemap.xml$', django.contrib.sitemaps.views.sitemap, {'sitemaps': sitemaps}),
    re_path(r'^robots.txt$', RobotsTxtView.as_view()),
    re_path(r'^(?P<path>(android-chrome|apple-touch|browserconfig|favicon|manifest|safari-pinned)[^/\.]*\.(json|png|ico|xml|svg))$',
        serve_web_file),

    # Monitoring API's
    path('api/health/', include(django_healthchecks.urls)),

    # CMS modules
    path('blog/comments/', include(fluent_comments.urls)),
    path('', include(fluent_pages.urls)),
]

if settings.DEBUG:
    # For runserver, also host the media files
    # Sass files are exported so browsers can open the Sass sources via sourcemaps.
    urlpatterns = [
        re_path(r'^media/(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        re_path(r'^sass/(?P<path>.*)$', django.views.static.serve, {'document_root': path.join(settings.SRC_DIR, 'frontend', 'sass'), 'show_indexes': True}),
    ] + urlpatterns

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        # Debug toolbar is explicitly linked, no magic that breaks on first request errors.
        import debug_toolbar
        urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
