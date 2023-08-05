# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SideBar(Component):
    """A SideBar component.
SideBar component
Dashboard > SideBar

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Used to render elements inside the component.

- id (string; default 'sidebar'):
    Used to identify dash components in callbacks.

- settings (list of strings; optional):
    Array of settings to render as component children.

- title (string; default 'Dashboard Settings'):
    Dashboard sidebar title."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, settings=Component.UNDEFINED, title=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'settings', 'title']
        self._type = 'SideBar'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'settings', 'title']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SideBar, self).__init__(children=children, **args)
