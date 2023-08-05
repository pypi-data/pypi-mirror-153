# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Table(Component):
    """A Table component.
Table component

Keyword arguments:

- id (string; default 'table'):
    Used to identify dash components in callbacks.

- columns (list of dicts; required):
    Array of table columns to render.

    `columns` is a list of dicts with keys:

    - field (string; optional):
        Column field.

    - width (number; optional):
        Column width.

- rows (list of dicts; optional):
    Array of table rows to render.

- rowsPerPageOptions (list of numbers; default [10, 25, 50]):
    Table pagination setting."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, columns=Component.REQUIRED, rows=Component.UNDEFINED, rowsPerPageOptions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'columns', 'rows', 'rowsPerPageOptions']
        self._type = 'Table'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'columns', 'rows', 'rowsPerPageOptions']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['columns']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Table, self).__init__(**args)
