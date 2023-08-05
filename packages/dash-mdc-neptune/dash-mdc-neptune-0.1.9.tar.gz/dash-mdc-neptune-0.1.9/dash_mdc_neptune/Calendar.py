# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Calendar(Component):
    """A Calendar component.
Calendar component

Keyword arguments:

- id (string; default 'calendar'):
    Used to identify dash components in callbacks.

- disableFuture (boolean; default True):
    Disable future dates.

- disablePast (boolean; default False):
    Disable past dates.

- helperText (string; optional):
    Text to display under the calendar form.

- labelText (string; optional):
    Text to display in the calendar form.

- maxDate (string; default '2100-01-01'):
    Latest date available in the calendar.

- minDate (string; default '1900-01-01'):
    Earliest date available in the calendar.

- selected (string; optional):
    Active date selection.

- width (string | number; default '100%'):
    Width of calendar form."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, helperText=Component.UNDEFINED, width=Component.UNDEFINED, maxDate=Component.UNDEFINED, minDate=Component.UNDEFINED, disableFuture=Component.UNDEFINED, disablePast=Component.UNDEFINED, selected=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'disableFuture', 'disablePast', 'helperText', 'labelText', 'maxDate', 'minDate', 'selected', 'width']
        self._type = 'Calendar'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'disableFuture', 'disablePast', 'helperText', 'labelText', 'maxDate', 'minDate', 'selected', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Calendar, self).__init__(**args)
