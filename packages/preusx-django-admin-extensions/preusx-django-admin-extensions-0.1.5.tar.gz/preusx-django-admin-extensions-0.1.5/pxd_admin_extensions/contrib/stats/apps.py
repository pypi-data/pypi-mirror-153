from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StatsConfig(AppConfig):
    name = 'pxd_admin_extensions.contrib.stats'
    label = 'pxd_admin_extensions_stats'
    verbose_name = _('Stats admin extension')
