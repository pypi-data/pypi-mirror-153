from typing import Optional
from functools import wraps

from django.contrib import admin


__all__ = (
    'using_kwarg_factory',
    'UsableAdminBaseMixin',
    'UsableForeignMixin',
    'UsableAdminMixin',
    'MultiDBModelAdmin',
)


def using_kwarg_factory(func):
    """Simple method wrapper to get a default using parameter.

    Args:
        func (Callable): Wrapped method.
    """
    def method(self, *args, using=None, **kwargs):
        return func(
            self, *args, using=self.using if using is None else using, **kwargs
        )

    return wraps(func)(method)


class UsableAdminBaseMixin:
    """Simpe mixin to apply default database key to the queryset resolver.

    ModelAdmin attribute `using` is for controlling which database
    the QuerySet will be evaluated against if you are using more than
    one database. The value is the alias of a database, as defined in DATABASES.
    """
    using: Optional[str] = None

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)


class UsableForeignMixin:
    """Mixin to add self `using` kwarg usage to ModelAdmin for foreign fields.
    """
    @using_kwarg_factory
    def formfield_for_foreignkey(self, *a, **k):
        return super().formfield_for_foreignkey(*a, **k)

    @using_kwarg_factory
    def formfield_for_manytomany(self, *a, **k):
        return super().formfield_for_manytomany(*a, **k)


class UsableAdminMixin(UsableAdminBaseMixin, UsableForeignMixin):
    pass


class MultiDBModelAdmin(UsableAdminMixin, admin.ModelAdmin):
    """Admin to search/create/change objects from non-default database.

    ModelAdmin attribute `using` is for controlling which database
    the QuerySet will be evaluated against if you are using more than
    one database. The value is the alias of a database, as defined in DATABASES.
    """
    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)
