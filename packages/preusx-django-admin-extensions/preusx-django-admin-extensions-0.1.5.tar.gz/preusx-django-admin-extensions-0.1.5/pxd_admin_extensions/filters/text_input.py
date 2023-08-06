from django.contrib.admin import FieldListFilter
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


__all__ = ('TextInputFilter',)


class TextInputFilter(FieldListFilter):
    """Renders simple eq admin filter form with text input and submit button.
    """
    parameter_name = None
    template = 'admin/text_input_filter.html'
    field = None

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(
            field, request, params, model, model_admin, field_path
        )

        self.field = field
        if self.parameter_name is None:
            self.parameter_name = self.field.name

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            self.used_parameters[self.parameter_name] = value

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})

    def value(self):
        """Returns the value (in string format) provided in the request's
        query string for this filter, if any. If the value wasn't provided then
        returns None.
        """
        return self.used_parameters.get(self.parameter_name, None)

    def has_output(self):
        return True

    def expected_parameters(self):
        """Returns the list of parameter names that are expected from the
        request's query string and that will be used by this filter.
        """
        return [self.parameter_name]

    def choices(self, cl):
        all_choice = {
            'selected': self.value() is None,
            'query_string': cl.get_query_string({}, [self.parameter_name]),
            'display': _('Clear'),
        }

        return ({
            'get_query': cl.params,
            'current_value': self.value(),
            'all_choice': all_choice,
            'parameter_name': self.parameter_name
        },)
