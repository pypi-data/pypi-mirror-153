__all__ = 'stat_legend', 'stat',


def stat_legend(key, title=None, **kwargs):
    """Simplifier for statistics legend definition.

    Args:
        key (str): Legend key.
        title (str, optional): Legend's title. Defaults to None.
    """
    return {'key': key, 'title': title or key, **kwargs}


def stat(
    title=None, legend=(), key=None, y=None, x=None, template_name=None,
    config={}
):
    """Statistics resolver method wrapper.
    Registers a new statistics block to display and with what inside.

    Args:
        title (str, optional): Block title. Defaults to None.
        legend (List[str], optional): List of field descriptors.
            Defaults to ().
        key (str, optional): Stat block unique key. Defaults to None.
        y (str, optional): Y axis key. Defaults to None.
        x (str, optional): X axis key. Defaults to None.
        template_name (str, optional): Django template name to use for block
            rendering.
            Defaults to None.
        config (dict, optional): Additional data to configure block.
            Defaults to {}.

    Example:
        ```python
        @register_stats(ExistingModelAdmin, model=ExistingModel)
        class ExistingModelStatsAdmin:
            @stat(_('Participants per domain'), (
                stat_legend('domain', _('Domain')),
                stat_legend('participants_count', _('Participants count')),
            ), config={'type': 'pie', 'labelType': 'percent'})
            def get_participants_per_domain(self, request, qs):
                return (
                    qs
                    .values('domain')
                    .annotate(participants_count=models.Count(
                        'participants__participant_id', distinct=True
                    ))
                    .order_by('domain')
                )
        ```

        By default every `stat` must return list of dicts with some valuable
        stats data. That will be then transformed using legend and config
        into a required chart.
    """
    assert len(legend) > 1, 'There must be at least 2 parameters to manage.'
    assert len(legend) < 4, 'We could match not more than 3 values at a time.'

    x = x or legend[0]['key']
    y = y or legend[1]['key']

    def wrapper(func):
        func.title = title
        func.template_name = template_name
        func.config = {'legend': legend, 'y': y, 'x': x, **config}
        func.key = key
        func.is_stat = True

        return func
    return wrapper
