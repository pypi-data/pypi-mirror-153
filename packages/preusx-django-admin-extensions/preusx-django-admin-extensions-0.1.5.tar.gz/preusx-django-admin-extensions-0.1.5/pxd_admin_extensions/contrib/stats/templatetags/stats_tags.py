import json
from django import template
from django.core.serializers.json import DjangoJSONEncoder

from ..const import STATS_POSTFIX

register = template.Library()


@register.filter
def stats_json(value):
    """Filter to transform stats into filter-understandable json.
    """
    return json.dumps(value, cls=DjangoJSONEncoder)


@register.filter
def add_to_list(array, to_add):
    """List push filter implementation.
    """
    if not isinstance(array, (list, tuple)):
        array = [array]

    return array + [to_add]


@register.filter
def is_in_column(value):
    """Checks whether the current 'i' is in the right column(out of some amount).
    """
    columns, col, i = value

    return i % columns == col


@register.simple_tag(takes_context=True)
def get_stats_link(context, back=False):
    """Generates link to a stats admin or vice versa.
    """
    stats_postfix = STATS_POSTFIX
    request = context['request']
    path = request.path[:-request.path.endswith('/')]
    url = request.get_full_path()
    changed_path = path[:-len(stats_postfix)] if back else path + stats_postfix

    return url.replace(path, changed_path)
