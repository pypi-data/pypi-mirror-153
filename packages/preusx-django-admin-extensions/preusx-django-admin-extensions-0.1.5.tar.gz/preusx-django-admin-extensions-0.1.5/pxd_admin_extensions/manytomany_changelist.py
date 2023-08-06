from typing import List, Sequence, Tuple, Union
from django.contrib.admin.views.main import ChangeList
from django import forms


__all__ = (
    'FieldsDefinition',
    'InjectableChangeList',
    'append_injector', 'after_injector',
    'make_form', 'make_view', 'make_admin_parts', 'make_admin_methods',
)

FieldsDefinition = List[
    Union[
        Tuple[str, forms.Field, callable],
        Tuple[str, forms.Field],
    ]
]


class InjectableChangeList(ChangeList):
    """ ChangeList view class with injection methods.
    """
    list_editable_injection_fields: FieldsDefinition = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.list_editable = [
            *self.list_editable,
            *(key for key, *_ in self.list_editable_injection_fields)
        ]

        self.list_display = self.inject_list_editable_fields(
            list(self.list_display), self.list_editable_injection_fields
        )

    def inject_list_editable_fields(
        self, source: List[str], fields: FieldsDefinition
    ):
        source = source[:]

        for key, _, injector in fields:
            source = injector(source, key)

        return source


def normalize_injection_fields(
    fields: FieldsDefinition, default_injector: callable
):
    """ Normalizes fields definition.
    """
    return [
        (
            definition[0],
            definition[1],
            definition[2] if len(definition) > 2 else default_injector
        )
        for definition in fields
    ]


def append_injector(sources: List[str], field: str):
    """ Simple injector that injects field at the end of the list.
    """
    return sources + [field]


def after_injector(after_field: str):
    """ Factory that returns an injector that injects field after the given field.
    """
    def injector(sources: List[str], field: str):
        index = sources.index(after_field) + 1

        return sources[:index] + [field] + sources[index:]

    return injector


def make_form(fields: FieldsDefinition, bases: Sequence[type] = []):
    """ Generates form class for the given fields.
    """
    bases = list(bases)

    if forms.ModelForm not in bases:
        bases.append(forms.ModelForm)

    return type('ChangelistForm', tuple(bases), {
        key: field
        for key, field, *_ in fields
    })


def make_view(
    fields: FieldsDefinition,
    default_injector: callable = append_injector,
    base_view_class: type = InjectableChangeList,
):
    """ Generates view class for the given fields.
    """
    return type('InjectableChangelistView', (base_view_class,), {
        'list_editable_injection_fields': normalize_injection_fields(
            fields, default_injector
        ),
    })


def make_admin_parts(
    fields: FieldsDefinition,
    default_injector: callable = append_injector,
    base_view_class: type = InjectableChangeList,
    form_bases: Sequence[type] = [],
):
    """
    Generates changelist form and view classes for the given fields.

    Args:
        fields (FieldsDefinition): List of fields definitions to inject.
        default_injector (callable, optional): Default injector function. Defaults to append_injector.
        base_view_class (type, optional): Base view class. Defaults to InjectableChangeList.
        form_bases (Sequence[type], optional): Base classes for resulting form. Defaults to [].

    Returns:
        Tuple: Form and view classes.
    """
    return (
        make_form(fields, form_bases),
        make_view(fields, default_injector, base_view_class)
    )


def make_admin_methods(
    fields: FieldsDefinition,
    default_injector: callable = append_injector,
    base_view_class: type = InjectableChangeList,
    form_bases: Sequence[type] = [],
):
    """
    Generates admin editable field injection methods for the given fields.

    Args:
        fields (FieldsDefinition): List of fields definitions to inject.
        default_injector (callable, optional): Default injector function. Defaults to append_injector.
        base_view_class (type, optional): Base view class. Defaults to InjectableChangeList.
        form_bases (Sequence[type], optional): Base classes for resulting form. Defaults to [].

    Returns:
        Tuple: Two methods: `get_changelist_form` and `get_changelist_view`.
    """
    form, view = make_admin_parts(
        fields, default_injector, base_view_class, form_bases
    )

    return (
        # get_changelist_form
        lambda *args, **kwargs: form,
        # get_changelist
        lambda *args, **kwargs: view,
    )
