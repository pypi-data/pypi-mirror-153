from django.contrib import admin

from .admin import StatsAdmin
from .const import STATS_POSTFIX


__all__ = (
    'create_simple_proxy_model',
    'register_stats',
)


ADMIN_STAT_ALTERNATIVES = {
    None: 'admin/stats_change_list.html',
    'admin/change_list.html': 'admin/stats_change_list.html',
    'admin_totals/change_list_totals.html': 'admin_totals/stats_change_list.html',
}


def create_simple_proxy_model(
    Model,
    postfix: str='Proxy',
    verbose_name: str=None,
    verbose_name_plural: str=None,
):
    """Factory to create "empty" proxy model.

    Args:
        Model (type): Base model to inherit from.
        postfix (str, optional): Postfix for model to have unique name.
            Defaults to 'Proxy'.
        verbose_name (str, optional): Model's verbose name. Defaults to None.
        verbose_name_plural (str, optional): Model's plural verbose name.
            Defaults to None.
    """
    v = verbose_name or Model._meta.verbose_name_raw
    vp = verbose_name_plural or Model._meta.verbose_name_plural

    class Meta:
        proxy = True
        verbose_name = v
        verbose_name_plural = vp

    return type(Model.__name__ + (postfix or 'Proxy'), (Model, ), {
        '__module__': Model.__module__,
        'Meta': Meta
    })


def register_stats(
    underlying_admin, registerer=admin.register, stats_admin=StatsAdmin,
    model=None, **kwargs
):
    """Factory to generate admin panel for statistics display.

    Args:
        underlying_admin (ModelAdmin): Current admin class.
        registerer (Callable, optional): Admin registerer.
            Defaults to admin.register.
        stats_admin (type, optional): Base class with admin statistics
            imlementation.
            Defaults to StatsAdmin.
        model (Model, optional): Model to add stats for. Defaults to None.
    """
    def wrapper(Class):
        postfix = STATS_POSTFIX
        Model = model or underlying_admin.model
        ProxyModel = create_simple_proxy_model(
            Model, 
            postfix=postfix,
            verbose_name=kwargs.pop('verbose_name', None),
            verbose_name_plural=kwargs.pop('verbose_name_plural', None)
        )
        Admin = type(
            underlying_admin.__name__,
            (stats_admin, Class, underlying_admin,),
            {
                'underlying_admin': underlying_admin,
                'underlying_admin': Model,
            }
        )
        underlying_admin.change_list_template = ADMIN_STAT_ALTERNATIVES.get(
            underlying_admin.change_list_template,
            underlying_admin.change_list_template
        )

        return registerer(ProxyModel, **kwargs)(Admin)

    return wrapper
