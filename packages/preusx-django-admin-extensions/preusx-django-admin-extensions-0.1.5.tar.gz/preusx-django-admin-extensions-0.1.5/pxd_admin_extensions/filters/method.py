from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


__all__ = ('MethodFilter',)


class MethodFilter(SimpleListFilter):
    """Simple admin filter to call queryset's method if selected as `yes`.
    """
    def lookups(self, request, model_admin):
        return (
            (None, _('No')),
            ('1', _('Yes')),
        )

    def queryset(self, request, queryset):
        if self.used_parameters.get(self.parameter_name) == '1':
            return getattr(queryset, self.method_name)()

        return queryset

    @classmethod
    def as_filter(cls, parameter_name: str, method: str = None, title=None):
        """Factory for easier filter generation.

        Args:
            parameter_name (str): Parameter to bind this filter.
            method (str, optional): Method to call. Defaults to None.
            title ([type], optional): Filters title. Defaults to None.
        """
        return type(parameter_name + 'Filter' + cls.__name__, (cls,), {
            'parameter_name': parameter_name,
            'method_name': method or parameter_name,
            'title': title or parameter_name
        })
