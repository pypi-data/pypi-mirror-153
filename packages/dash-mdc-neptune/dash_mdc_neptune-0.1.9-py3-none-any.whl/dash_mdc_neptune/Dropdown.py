# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Dropdown(Component):
    """A Dropdown component.
Dropdown component

Keyword arguments:

- id (string; default 'select'):
    Used to identify dash components in callbacks.

- helperText (string; optional):
    Text to display under the dropdown form.

- labelText (string; optional):
    Text to display in the dropdown form, when no items are selected.

- multiple (boolean; default True):
    Allow multiple selections.

- options (list of string | numbers; required):
    Array of options to select in the dropdown form.

- selected (list of string | numbers; optional):
    Active option selection.

- width (string | number; default '100%'):
    Width of dropdown form."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, helperText=Component.UNDEFINED, width=Component.UNDEFINED, options=Component.REQUIRED, multiple=Component.UNDEFINED, selected=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'helperText', 'labelText', 'multiple', 'options', 'selected', 'width']
        self._type = 'Dropdown'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'helperText', 'labelText', 'multiple', 'options', 'selected', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['options']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Dropdown, self).__init__(**args)
