from typing import Sequence
from functools import reduce

from django.db import models
from django.http.request import HttpRequest


__all__ = ('ListAnnotatorAdminMixin',)


class ListAnnotatorAdminMixin:
    """Mixin to easily add annotated fields to a select.

    Property `list_annotations` may be filled with an annotations definitions:

    Example:
        ```python
        class SomeAdmin:
            list_annotations = (
                ('participants', models.Count, 'participants_count'),
            )
        ```

        Where:

        - The field name to manupulate(might be None if function does not require it to be).
        - The second parameter is the callable that receives field and
            does something with it.
            Must return data that can be used as annotation.
        - Third parameter - is the resulting field name. May not be present,
            in that case the name will be `self.LIST_ANNOTATIONS_PREFIX + field`.
    """
    LIST_ANNOTATIONS_PREFIX: str = 'annotated_'
    list_annotations: Sequence = ()

    def _resolve_annotation_definition(self, map: dict, definition: Sequence):
        field, func, *_ = definition
        name = (
            definition[2]
            if len(definition) >= 3 else
            self.LIST_ANNOTATIONS_PREFIX + field
        )
        map[name] = func(field)

        return map

    def get_queryset(self, request: HttpRequest) -> models.QuerySet:
        q = super().get_queryset(request)
        annotations: dict = reduce(
            self._resolve_annotation_definition,
            self.get_list_annotations(request, q),
            {}
        )

        return q.annotate(**annotations)

    def get_list_annotations(
        self, request: HttpRequest, queryset: models.QuerySet
    ) -> Sequence:
        return self.list_annotations
