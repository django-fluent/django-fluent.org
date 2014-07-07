import json
from urllib2 import urlopen, HTTPError
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import PluginImageField, PluginHtmlField, PluginUrlField
from fluent_contents.models import ContentItem


class Col12Item(ContentItem):
    """
    A column that takes 1/2 of the width
    """
    title = models.CharField(_("Title"), max_length=200)
    icon = PluginImageField(_("Icon"), blank=True)
    body = PluginHtmlField(_("Body"))

    class Meta:
        verbose_name = _("Column (1/2)")
        verbose_name_plural = _("Columns (1/2)")

    def __unicode__(self):
        return self.title


class ContentBoxItem(ContentItem):
    """
    The context box includes a divider.
    """
    class Meta:
        verbose_name = _("Content box splitter")
        verbose_name_plural = _("Content box splitters")

    def __unicode__(self):
        return u'splitter'


class ImageTextItem(ContentItem):
    """
    A block with image + text
    """
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'
    ALIGN_CHOICES = (
        (ALIGN_LEFT, _("Left")),
        (ALIGN_RIGHT, _("Right")),
    )

    title = models.CharField(_("Title"), max_length=200)
    image = PluginImageField(_("Image"))
    align = models.CharField(_("Align"), max_length=10, choices=ALIGN_CHOICES, default=ALIGN_LEFT)
    body = PluginHtmlField(_("Body"))

    url = PluginUrlField(_("URL"), blank=True)
    url_text = models.CharField(_("Text"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("Image+text")
        verbose_name_plural = _("Image+text items")

    def __unicode__(self):
        return self.title

    @property
    def image_css_class(self):
        if self.align == self.ALIGN_RIGHT:
            return 'image_fr'
        else:
            return 'image_fl'


class PackageItem(ContentItem):
    """
    An item on the page that describes a Python package.
    """
    slug = models.SlugField(_("Slug"))
    repository_url = models.URLField("Repository URL")

    description = models.TextField(_("Description"))
    homepage = models.URLField("Homepage", help_text=_("You only have to enter a homepage URL for external packages"), blank=True)

    # Fetched at save:
    rtd_html_url = models.URLField(_("RTD URL"), editable=False, blank=True)

    class Meta:
        verbose_name = _("Python Package item")
        verbose_name_plural = _("Python Package items")
        ordering = ('slug',)


    def __unicode__(self):
        return self.slug


    def save(self, *args, **kwargs):
        if not self.rtd_html_url:
            rtd_info = self.rtd_info
            if rtd_info:
                self.rtd_html_url = rtd_info['subdomain']
        super(PackageItem, self).save(*args, **kwargs)


    @property
    def is_external(self):
        return not self.repository_url.startswith('https://github.com/{0}/'.format(settings.PACKAGEITEM_INTERNAL_GITHUB_ORG))


    @property
    def repository_name(self):
        """
        Return a Human readable name for the repository hosting site.
        """
        if not self.repository_url:
            return _("(None)")
        if 'github.com/' in self.repository_url:
            return "GitHub"
        if 'bitbucket.org/' in self.repository_url:
            return "Bitbucket"
        if 'code.google.com/' in self.repository_url:
            return "Google Code"
        return _("Unknown")


    @cached_property
    def rtd_info(self):
        """
        Return the information from Read the Docs.
        """
        cachekey = 'readthedocs.projectinfo.{0}'.format(self.slug)
        return _fetch_json(cachekey, 'http://readthedocs.org/api/v1/project/{slug}/?format=json'.format(slug=self.slug))


    @property
    def rtd_subdomain(self):
        return self.rtd_info['subdomain'] if self.rtd_info else None


    @cached_property
    def github_info(self):
        """
        Return the information from GitHub.
        """
        if 'github.com' not in self.repository_url:
            return None

        org, repos = self.repository_url.split('/')[3:5]  # 'https://github.com/org/repos/'
        cachekey = 'github.repositoryinfo.{0}.{1}'.format(org, repos)
        return _fetch_json(cachekey, 'https://api.github.com/repos/{0}/{1}'.format(org, repos))


    @property
    def github_description(self):
        return self.github_info['description'] if self.github_info else None



def _fetch_json(cachekey, url, ignore_status=(404,)):
    """
    Fetch a json object, cache it in memcache.
    """
    json = cache.get(cachekey)
    if not json:
        try:
            response = urlopen(url)
        except HTTPError as e:
            if e.code in ignore_status:
                cache.set(cachekey, None)
                return None
            raise
        else:
            json = json.loads(response.read())
            cache.set(cachekey, json)
    return json
