# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Section(Component):
    """A Section component.
Section component
Dashboard > Page > Section

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Used to render elements inside the component.

- id (string; default 'section'):
    Used to identify dash components in callbacks.

- cards (list of dicts; optional):
    Array of cards to render as component children.

    `cards` is a list of dicts with keys:

    - downloadable (boolean; optional):
        Card dowloadable.

    - size (number; optional):
        Card size (0 < size <= 12).

    - title (string; optional):
        Card title.

- downloaded (number; default 0):
    Section download counter.

- orientation (a value equal to: 'columns', 'rows'; default 'rows'):
    Section general orientation (rows or columns).

- size (number; optional):
    Section container size (0 < size <= 12)."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, cards=Component.UNDEFINED, size=Component.UNDEFINED, orientation=Component.UNDEFINED, downloaded=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'cards', 'downloaded', 'orientation', 'size']
        self._type = 'Section'
        self._namespace = 'dash_mdc_neptune'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'cards', 'downloaded', 'orientation', 'size']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Section, self).__init__(children=children, **args)
