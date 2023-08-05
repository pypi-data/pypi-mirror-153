# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Tab(Component):
    """A Tab component.
Tab component
Dashboard > Page > Section > Card > Tab
https://github.com/danielfrg/jupyter-flex/blob/main/js/src/Section/index.js

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Used to render elements inside the component.

- id (string; default 'tab'):
    Used to identify dash components in callbacks.

- tabs (list of dicts; optional):
    Array of tabs to render as component children.

    `tabs` is a list of dicts with keys:

    - label (string; optional):
        Element label."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, tabs=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'tabs']
        self._type = 'Tab'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'tabs']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Tab, self).__init__(children=children, **args)
