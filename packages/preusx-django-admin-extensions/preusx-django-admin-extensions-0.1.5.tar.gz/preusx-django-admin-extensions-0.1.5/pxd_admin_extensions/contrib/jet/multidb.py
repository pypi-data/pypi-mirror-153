from jet.admin import CompactInline

from ...multidb import UsableAdminMixin


__all__ = ('MultiDBCompactInline',)


class MultiDBCompactInline(UsableAdminMixin, CompactInline):
    """Compact inline for multidb usage.
    """
    pass
