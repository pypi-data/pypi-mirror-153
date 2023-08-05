# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toggle(Component):
    """A Toggle component.
Toggle component

Keyword arguments:

- id (string; default 'toggle'):
    Used to identify dash components in callbacks.

- options (list of string | numbers; required):
    Array of options to select through the toggle.

- orientation (a value equal to: 'horizontal', 'vertical'; default 'horizontal'):
    Toggle orientation (horizontal or vertical).

- selected (string | number; optional):
    Selected toggle index."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, orientation=Component.UNDEFINED, options=Component.REQUIRED, selected=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'options', 'orientation', 'selected']
        self._type = 'Toggle'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'options', 'orientation', 'selected']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Toggle, self).__init__(**args)
