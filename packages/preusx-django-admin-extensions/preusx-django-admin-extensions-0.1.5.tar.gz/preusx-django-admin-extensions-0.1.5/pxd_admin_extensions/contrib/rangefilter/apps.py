from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RangeFilterExtensionConfig(AppConfig):
    name = 'pxd_admin_extensions.contrib.rangefilter'
    label = 'pxd_admin_extensions_rangefilter'
    verbose_name = _('Range filter admin extension')
