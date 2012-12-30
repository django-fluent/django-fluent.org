from django.contrib.admin.widgets import AdminTextareaWidget
from django.utils.translation import ugettext_lazy as _
from fluent_contents.extensions import ContentPlugin, plugin_pool
from .models import PackageItem


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
