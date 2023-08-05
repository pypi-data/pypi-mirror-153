# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Box(Component):
    """A Box component.
Box component from Material UI
https://mui.com/components/box/

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Can be used to render elements inside the component.

- sx (dict; optional):
    All Material system properties are available via the `sx prop`
    Allow additional css styles to be applied to the component."""
    @_explicitize_args
    def __init__(self, children=None, sx=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'sx']
        self._type = 'Box'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'sx']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Box, self).__init__(children=children, **args)
