from django.contrib import admin
from pxd_admin_extensions import ChangeListCustomTemplateNameAdminMixin


__all__ = (
    'ViewOnlyAdminMixin',
    'StatsAdmin',
)


class ViewOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StatsAdmin(
    ViewOnlyAdminMixin,
    ChangeListCustomTemplateNameAdminMixin,
    admin.ModelAdmin
):
    """Admin basement for stats interface.
    """
    change_list_template_name = 'stats_list'
    stat_display_default_template_name = 'admin/includes/stats/display.html'
    stat_columns_amount = 2
    underlying_admin = None
    underlying_model = None

    class Media:
        css = {'all': ('admin/stats/nv.d3.min.css',)}
        js = (
            'admin/stats/d3.min.js', 'admin/stats/nv.d3.min.js',
            'admin/stats/chart.js',
        )

    def get_stats_date_period(self, request, date_hierarchy=None):
        """Simple method to resolve date truncation basedon the date
        hierarchy filter.
        """
        date_hierarchy = date_hierarchy or self.date_hierarchy

        if date_hierarchy + '__day' in request.GET:
            return 'minute'
        if date_hierarchy + '__month' in request.GET:
            return 'day'
        if date_hierarchy + '__year' in request.GET:
            return 'month'

        return 'year'

    def collect_stats(self, request, qs):
        """Collects all the defined stat callers and executes them.
        """
        attributes = ((key, getattr(self, key)) for key in dir(self))
        stat_callables = (
            (key, attr) for key, attr in attributes
            if callable(attr) and hasattr(attr, 'is_stat') and attr.is_stat
        )
        key_normalized = (
            (
                attr.key if hasattr(attr, 'key') and attr.key else
                key[key.startswith('get_') and 4 or 0:],
                attr
            )
            for key, attr in stat_callables
        )

        return [
            {
                'key': k,
                'result': list(attr(request, qs)),
                'config': getattr(attr, 'config', None) or {},
                'template_name': (
                    getattr(attr, 'template_name', None) or
                    self.stat_display_default_template_name
                ),
                'title': getattr(attr, 'title', None) or k,
            }
            for k, attr in key_normalized
        ]

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request, extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['stats'] = self.collect_stats(request, qs)
        response.context_data['stats_columns'] = list(range(min(
            self.stat_columns_amount, len(response.context_data['stats'])
        )))

        return response
