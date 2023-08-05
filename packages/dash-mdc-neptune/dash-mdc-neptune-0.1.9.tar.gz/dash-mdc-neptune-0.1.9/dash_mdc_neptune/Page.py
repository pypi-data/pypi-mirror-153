# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Page(Component):
    """A Page component.
Page component, used to wrap section and card components
Dashboard > Page

Keyword arguments:

- children (optional):
    Used to render elements inside the component.

- id (default 'page'):
    Used to identify dash components in callbacks.

- orientation (default 'columns'):
    Page general orientation (rows or columns)."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, orientation=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'orientation']
        self._type = 'Page'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'orientation']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Page, self).__init__(children=children, **args)
