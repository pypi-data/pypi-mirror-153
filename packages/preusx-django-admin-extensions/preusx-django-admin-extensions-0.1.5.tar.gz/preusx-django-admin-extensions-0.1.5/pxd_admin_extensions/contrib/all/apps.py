from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AllExtensionConfig(AppConfig):
    name = 'pxd_admin_extensions.contrib.all'
    label = 'pxd_admin_extensions_all'
    verbose_name = _('All contrib together app')
