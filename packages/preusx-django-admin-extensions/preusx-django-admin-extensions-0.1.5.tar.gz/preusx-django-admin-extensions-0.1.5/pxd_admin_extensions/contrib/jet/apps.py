from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JetExtensionConfig(AppConfig):
    name = 'pxd_admin_extensions.contrib.jet'
    label = 'pxd_admin_extensions_jet'
    verbose_name = _('Jet admin extension')
