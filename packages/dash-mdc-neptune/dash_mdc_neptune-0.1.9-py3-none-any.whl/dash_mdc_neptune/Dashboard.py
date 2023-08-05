# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dashboard(Component):
    """A Dashboard component.
Main dasboard component, initializing a Material UI theme
https://mui.com/customization/theming/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Used to render elements inside the component.

- id (string; default 'dashboard'):
    Used to identify dash components in callbacks.

- height (string; default '100vh'):
    Dashboard window height."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'height']
        self._type = 'Dashboard'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'height']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dashboard, self).__init__(children=children, **args)
