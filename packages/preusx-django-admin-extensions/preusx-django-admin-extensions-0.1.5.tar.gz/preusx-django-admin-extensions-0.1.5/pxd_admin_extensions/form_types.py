__all__ = 'FormTypeAdminMixin',


class FormTypeAdminMixin:
    """Mixin that let you use different forms for different object
    manupulation scenarios:

    - `changelist_form` - Special form for changelist admin view.
    - `add_form` - Special form for object creation.
    - `change_form` - Special form for object update mechanics.

    All those forms will fallback to a default one if none provided.
    """
    def get_form(self, request, obj=None, **kwargs):
        form = getattr(
            self, 'add_form' if obj is None else 'change_form', self.form
        ) or self.form

        if form is not None:
            kwargs.setdefault('form', form)

        return super().get_form(request, obj, **kwargs)

    def get_changelist_form(self, request, **kwargs):
        form = getattr(self, 'changelist_form', self.form) or self.form

        if form is not None:
            kwargs.setdefault('form', form)

        return super().get_changelist_form(request, **kwargs)
