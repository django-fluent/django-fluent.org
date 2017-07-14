from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import ContentPlugin, plugin_pool
from .models import Col12Item, ContentBoxItem, ImageTextItem, PackageItem


@plugin_pool.register
class Col12Plugin(ContentPlugin):
    model = Col12Item
    render_template = "themeelements/col12.html"
    category = _("Theme elements")


@plugin_pool.register
class ContentBoxPlugin(ContentPlugin):
    model = ContentBoxItem
    render_template = "themeelements/contentbox.html"
    category = _("Theme elements")


@plugin_pool.register
class ImageTextPlugin(ContentPlugin):
    model = ImageTextItem
    render_template = "themeelements/imagetext.html"
    category = _("Theme elements")
    radio_fields = {
        'align': ContentPlugin.HORIZONTAL,
    }

    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'align', 'body',)
        }),
        (_("Read more link"), {
            'fields': ('url', 'url_text',)
        })
    )


@plugin_pool.register
class PackagePlugin(ContentPlugin):
    model = PackageItem
    render_template = "themeelements/packageitem.html"
    category = _("Theme elements")

    formfield_overrides = {
        'description': {
            'widget': AdminTextareaWidget(attrs={'rows': 4, 'style': 'width: 30em;'})
        }
    }

    class Media:
        js = (
            'themeelements/admin/packageplugin.js',
        )
