__all__ = 'ChangeListCustomTemplateNameAdminMixin',


class ChangeListCustomTemplateNameAdminMixin:
    """Simple mixin to made auto-generatable template paths out of template name.

    It mimics default django admin template resolving behavior, but it changes
    default `change_list` template name to thw one from
    `self.change_list_template_name` attribute.
    """
    change_list_template_name = 'change_list'

    @property
    def change_list_template(self):
        name = self.change_list_template_name
        opts = self.model._meta
        app_label = opts.app_label

        return [
            f'admin/{app_label}/{opts.model_name}/{name}.html',
            f'admin/{app_label}/{name}.html',
            f'admin/{name}.html'
        ]
