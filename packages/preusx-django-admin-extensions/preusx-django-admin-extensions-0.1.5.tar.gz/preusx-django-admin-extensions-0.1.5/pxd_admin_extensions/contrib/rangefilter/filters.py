from datetime import datetime

from psycopg2.extras import DateTimeRange
from django.utils.translation import ugettext_lazy as _
from rangefilter.filter import DateTimeRangeFilter


__all__ = ('DateTimeRangeForRangeFilter',)


class DateTimeRangeForRangeFilter(DateTimeRangeFilter):
    """Date range filter for no-timezone dates.
    """
    def _make_query_filter(self, request, validated_data):
        gte: datetime = validated_data.get(self.lookup_kwarg_gte, None)
        lte: datetime = validated_data.get(self.lookup_kwarg_lte, None)

        return {
            f'{self.field_path}__overlap': DateTimeRange(
                gte.replace(tzinfo=None),
                lte.replace(tzinfo=None),
                bounds='[]'
            )
        }
