'''Models to store complex information in unambiguous ways.

Mostly implemented as `dataclasses`.
'''
import logging
import warnings
from dataclasses import dataclass, field as dc_field, fields, astuple as dc_astuple, replace as dc_replace, asdict as dc_asdict, InitVar
import enum
import abc
from functools import cached_property
import math
from pathlib import Path
from fractions import Fraction
import tkinter as tk
import typing

from . import util

if typing.TYPE_CHECKING:
    # Avoid circular imports
    from . import mixin
    from . import EntryMultiline


vsT = typing.TypeVar('vsT')
wsT = typing.TypeVar('wsT')
wsST = typing.TypeVar('wsST')
TraceModeT = typing.Literal['read', 'write', 'unset']
'''The supported operations to watch for a trace.

There is no Python documentation, see ``Tk`` `trace variable <https://www.tcl.tk/man/tcl/TclCmd/trace.html#M14>`_ documentation.
'''


# Image Types
__image_types = {
}
# TODO: Support more image types with Pillow:
# - See https://pillow.readthedocs.io/en/stable/reference/ImageTk.html
# PNG is only supported on "tk8.6"
# - Gated by Tk version
if util.TK_VERSION >= (8, 6):
    __image_types['png'] = tk.PhotoImage
# GIF is supported everywhere
__image_types['gif'] = tk.PhotoImage

IMAGE_TYPES = __image_types
'''Supported image types, and corresponding loaders.

See `ImageCache`.
'''


logger = logging.getLogger(__name__)
logger_layout = logging.getLogger('%s.layout' % __name__)


class FileType(typing.Tuple[str]):
    def __new__(cls, *args: str):
        true_args = (f'.{s}' for s in args)
        return super().__new__(cls, true_args)  # type: ignore

    def matches(self, path: Path):
        if __debug__:
            suff = tuple(path.suffixes[-len(self):])
            res = '==' if self == suff else '<=>'
            logger.debug(f'F[{path}]={suff} {res} {self}')
        return path.name.endswith(self.suffix)

    @cached_property
    def suffix(self):
        return ''.join(self)

    @cached_property
    def pattern(self):
        return f'*{self.suffix}'


class FileTypes(typing.Dict[str, FileType]):
    def allbut(self, *keys: str):
        return {k: v for k, v in self.items() if k not in keys}

    def only(self, *keys: str):
        return {k: self[k] for k in keys}


@dataclass
class WStyle:
    '''Widget style object.

    This is super class of all widget-specific style objects.

    All subclass arguments should be optional, with a nice-looking default
    value.

    Args:
        _default: Does this represent a default value?
            When this is set (only for class ``__init___`` definitions), the
            values can be safely overriden.

    Note:
        Not to be confused with `tkinter.ttk.Style` objects.
    '''
    _default: bool = dc_field(repr=False, compare=False, default=False)


class CP(enum.Enum):
    '''A Cardinal Point.

    Usually, this defines an anchor point for alignment.

    Corresponds neatly to the same `tkinter` values, but it's simpler to validate
    as an `enum`.
    '''
    # value: typing.Optional[str]  # TODO: Improve labelAnchor usages?

    N = tk.N
    S = tk.S
    E = tk.E
    W = tk.W
    NE = tk.NE
    NW = tk.NW
    SE = tk.SE
    SW = tk.SW
    default = None
    '''OS-specific cardinal point.'''


CP_Compound: typing.Mapping[typing.Union[CP, bool, None], str] = {
    CP.default: 'none',  # `image` if present, otherwise `text`
    CP.N: tk.BOTTOM,
    CP.S: tk.TOP,
    CP.E: tk.LEFT,
    CP.W: tk.RIGHT,
    # Special Compound values
    True: 'image',  # No Label, only Image
    False: 'text',  # No Image, only Label
    None: 'center',  # Image and Label, centered
}
'''The ``compound`` configuration setting.

This is the mapping between `CP` and the ``compound`` configuration string used in several locations.

There is no Python documentation, see ``Tk`` `compound <https://www.tcl.tk/man/tcl/TkCmd/ttk_widget.html#M-compound>`_ documentation.
'''


@dataclass
class PixelSize:
    width: int
    height: int

    @property
    def aspect_ratio(self):
        return Fraction(self.width, self.height)

    tuple = dc_astuple
    '''Get this information as a tuple.'''

    def reduce(self, ratio):
        return dc_replace(self, width=self.width // ratio, height=self.height // ratio)


@dataclass
class GridCoordinates:
    '''Widget Grid Coordinates.

    This includes information about widgets that span more than one row or
    column. It should fully specify the widget grid location.

    The "location string" format is the following: ``R[+RS]xC[+CS]``

    - **R**: Row
    - **RS**: Row Span (optional)
    - **C**: Column
    - **CS**: Column Span (optional)

    .. automethod:: __str__
    '''
    row: int
    column: int
    rowspan: int = 1
    columnspan: int = 1

    dict = dc_asdict
    '''Get this information as a dictionary.'''

    tuple = dc_astuple
    '''Get this information as a tuple.

    Note:
        The order of fields is not ideal.
    '''

    def __str__(self):
        '''Convert the grid coordinates into a "location string".

        For the reverse operation, see `parse`.
        '''
        _row = '%d+%d' % (self.row, self.rowspan)
        _col = '%d+%d' % (self.column, self.columnspan)
        return ('%sx%s' % (_row, _col)).replace('+1', '')

    @classmethod
    def parse(cls, string: str) -> 'GridCoordinates':
        '''Parse a "location string" to a grid coordinates object.

        For the reverse operation, convert the object to `str` (see `__str__`).
        '''
        r, c = string.split('x')
        if '+' in r:
            row, rowspan = [int(n) for n in r.split('+')]
        else:
            row = int(r)
            rowspan = 1
        if '+' in c:
            column, columnspan = [int(n) for n in c.split('+')]
        else:
            column = int(c)
            columnspan = 1
        return cls(row, column, rowspan=rowspan, columnspan=columnspan)


@dataclass
class GridSize:
    rows: int
    columns: int

    tuple = dc_astuple
    '''Get this information as a tuple.'''


@dataclass
class ImageCache:
    '''Image Cache metadata.

    Each cached image has metadata associated with it, to be able to support
    lazy-loading images.

    The ``obj`` point to the image object, the rest are metadata used to
    reconstruct it.
    '''
    # Cached
    obj: typing.Optional[tk.Image] = None
    # UnCached
    fname: typing.Optional[Path] = None
    data: typing.Optional[bytes] = None
    dtype: typing.Optional[str] = None

    def __post_init__(self):
        assert self.dtype is None or self.dtype in IMAGE_TYPES

    @property
    def cached(self) -> bool:
        '''Check if the image object is cached.'''
        return self.obj is not None


class Direction(enum.Enum):
    '''Hold the direction of automatic widget layout.

    The possible values are the cardinal directions:

    +-----+-----+-----+
    |*Cardinal Point* |
    +-----+-----+-----+
    |     |  N  |     |
    +-----+-----+-----+
    |  W  |     |  E  |
    +-----+-----+-----+
    |     |  S  |     |
    +-----+-----+-----+

    - **N**: North
    - **S**: South
    - **E**: East
    - **W**: West

    '''
    # deltaRow, deltaColumn
    N = (-1, 0)
    S = (+1, 0)
    E = (0, +1)
    W = (0, -1)

    def __init__(self, dR: int, dC: int):
        # This is not really used anywhere, for now
        # It requires complex modulo-with-carry calculations
        self.dR = dR
        self.dC = dC
        assert len(self.name) == 1, 'Direction name must be a single character'

    def grid(self, rows: int, cols: int, amount: typing.Optional[int] = None, auto_fill: bool = True) -> typing.Iterable[GridCoordinates]:
        '''Generate `GridCoordinates` for a widget grid.

        If the ``amount`` of widgets to distribute is not given, this assumes the
        coordinates are calculated for an uniform grid (all spaces occupied).

        This ``amount`` must fit on the grid, which mean rejecting amounts of
        widgets that leave an entire row or column unfilled. The
        ``auto_fill`` flag controls adjusting the last widget to completely
        fill the available space.

        Args:
            rows: Number of rows on the grid
            cols: Number of columns on the grid
            amount: Number of widgets to distribute. Optional, defaults to
                having all the grid positions fulfilled.
            auto_fill: Adjust the missing widgets by expanding the last one
                to fill the rest of the empty space. Defaults to enable.
        '''
        size = rows * cols
        amount = amount or size
        if amount > size:
            raise ValueError('Too many widgets in too few locations')
        extra_size = size - amount
        if self.dR != 0 and extra_size >= rows:
            raise ValueError('Too few widgets for this grid: empty columns')
        if self.dC != 0 and extra_size >= cols:
            raise ValueError('Too few widgets for this grid: empty rows')
        if __debug__:
            logger_layout.debug('Grid[%s]: %d (%dx%d=%d) [D%d]', self.name, amount, rows, cols, size, extra_size)
        for idx in range(amount):
            if self in (Direction.E, Direction.W):  # Horizontal
                c = (idx // cols, idx % cols)
            elif self in (Direction.N, Direction.S):  # Vertical
                c = (idx % rows, idx // rows)
            else:
                # Not generic for any delta...
                raise NotImplementedError
            crspan, ccspan = 1, 1
            crow = rows - 1 - c[0] if self.dR < 0 else c[0]
            ccol = cols - 1 - c[1] if self.dC < 0 else c[1]
            if auto_fill and extra_size > 0 and idx == amount - 1:
                if self == Direction.N:
                    crow = crow - extra_size
                    crspan = 1 + extra_size
                elif self == Direction.S:
                    crspan = 1 + extra_size
                elif self == Direction.E:
                    ccspan = 1 + extra_size
                elif self == Direction.W:
                    ccol = ccol - extra_size
                    ccspan = 1 + extra_size
                assert 0 <= crow <= rows and 0 <= crow + crspan - 1 <= rows
                assert 0 <= ccol <= cols and 0 <= ccol + ccspan - 1 <= cols
            if __debug__:
                logger_layout.debug('»» %d | %d+%dx%d+%d || %dx%d', idx, crow, crspan, ccol, ccspan, *c)
            yield GridCoordinates(crow, ccol,
                                  rowspan=crspan, columnspan=ccspan)

    def multiples(self, *amounts: typing.Optional[int], amount: typing.Optional[int] = None) -> typing.Iterable[GridCoordinates]:
        '''Generate `GridCoordinates` for sequence of integer amounts.

        ``amounts`` is a series of integers or `None` (refered to as "slots"),
        to be distributed per row/column, depending on the direction.

        There can be any number of "slots", marking a row/column as receiving
        the remaining widgets. The remaining widgets are distributed evenly
        through the existing "slots".

        If the ``amount`` of widgets to distribute is not given, there is no
        support for using `None` as amount. Another possible error is giving an
        amount of slots that do not evenly divide the remaining widgets.

        Args:
            amounts: Amount of widgets per row/column.
            amount: Number of widgets to distribute. Optional.
        '''
        if __debug__:
            logger_layout.debug('Multiple: (%s)[%s]', ' '.join(str(a or 'x') for a in amounts), amount)
        size: int
        if amount is None:
            if None in amounts:
                raise ValueError('"x" requires all `amounts` to be defined')
            # `amounts` has no `None` elements now
            size = sum(typing.cast(typing.Sequence[int], amounts))
            amount = size
        else:
            amount_x = amounts.count(None)
            if amount_x > 0:
                existing_amount = typing.cast(int, sum((a or 0 for a in amounts)))
                remaining_amount = amount - existing_amount
                delta = math.ceil(remaining_amount / amount_x)
                if delta * amount_x != remaining_amount:
                    raise ValueError(f'Unable to distribute {remaining_amount} by {amount_x} slots')
                if __debug__:
                    logger_layout.debug('- Slots : %ds * %d/s = %d', amount_x, delta, remaining_amount)
                amounts = tuple(delta if a is None else a for a in amounts)
            # `amounts` has no `None` elements now
            size = sum(typing.cast(typing.Sequence[int], amounts))
        asize, osize = len(amounts), util.lcm_multiple(*amounts)
        if __debug__:
            logger_layout.debug('- Sizes : A%d O%d = %d', asize, osize, asize * osize)
        # assert isinstance(amount, int)
        if amount > size:
            raise ValueError('Too many widgets for these amounts')
        elif amount < size:
            raise ValueError('Too few widgets for these amounts')
        for idx, this_amount in enumerate(amounts):
            this_width = osize // this_amount
            for other in range(0, osize, this_width):
                if __debug__:
                    logger_layout.debug('» T%d O%d TW%d | TA%d OS%d', idx, other, this_width, this_amount, osize)
                if self in (Direction.E, Direction.W):  # Horizontal
                    # Grid: asize x osize
                    crow, ccol, crspan, ccspan = idx, other, 1, this_width
                    if self.dC < 0:
                        ccol = osize - ccol - ccspan
                    assert 0 <= crow <= asize and 0 <= crow + crspan - 1 <= asize
                    assert 0 <= ccol <= osize and 0 <= ccol + ccspan - 1 <= osize
                elif self in (Direction.N, Direction.S):  # Vertical
                    # Grid: osize x asize
                    crow, ccol, crspan, ccspan = other, idx, this_width, 1
                    if self.dR < 0:
                        crow = osize - crow - crspan
                    assert 0 <= crow <= osize and 0 <= crow + crspan - 1 <= osize
                    assert 0 <= ccol <= asize and 0 <= ccol + ccspan - 1 <= asize
                if __debug__:
                    logger_layout.debug('»» %d %d | %d+%dx%d+%d', idx, other, crow, crspan, ccol, ccspan)
                yield GridCoordinates(crow, ccol,
                                      rowspan=crspan, columnspan=ccspan)


@dataclass
class WidgetDynamicState:
    '''Hold the dynamic state for a widget.

    See `mixin.MixinState`.

    Args:
        getter: Function to retrieve the state
        setter: Function to change the state
        noneable: Is this widget noneable? See `mixin.MixinState.isNoneable`.
        container: Is this widget a container? Defaults to `False`.
    '''
    getter: typing.Callable
    setter: typing.Callable
    noneable: bool
    container: bool = False

    def __str__(self):
        strs = []
        if self.container:
            strs.append('C')
        if self.noneable:
            strs.append('N')
        strings = ','.join(strs)
        # TODO: Use `self.__class__.__name__`
        return f'WDS[{strings}]'


@dataclass
class VState(typing.Generic[vsT]):
    '''Hold validated state.

    This is needed to make sure the received object is really a validated
    state, or just any regular state.
    '''

    value: vsT
    '''The validated value.'''
    label: typing.Optional[str] = None
    '''The label present on the widget; Optional.'''

    dict = dc_asdict
    '''Get this information as a dictionary.'''


@dataclass
class WState(typing.Generic[wsT, wsST]):
    '''Hold wrapped state.

    This is needed to mark state as being a product of a wrapped container.
    '''

    state: typing.Optional[wsT]
    '''The widget state.

    This is the extra value being stored on the widget.
    Optional, if the variable already exists upstream.
    '''
    substate: wsST
    '''The wrapped state.

    This is the original value being stored on the widget.
    '''

    dict = dc_asdict
    '''Get this information as a dictionary.'''


@dataclass
class GuiState:
    '''Widget GUI state.

    This supports all possible states, not all widgets support all states.

    See `GUI_STATES`, `mixin.MixinWidget.gstate`.
    '''
    enabled: typing.Optional[bool] = None
    valid: typing.Optional[bool] = None
    readonly: typing.Optional[bool] = None

    def items(self):
        '''Workaround for `dataclasses.asdict` issue.

        This is a problem-free version of:

        .. code:: python

            return dataclasses.asdict(self).items()
        '''
        for f in fields(self):
            yield (f.name, getattr(self, f.name))

    def items_tk(self):
        '''
        Version of `items` that includes the ``Tk`` string, available in
        `GUI_STATES`.

        The ``Tk`` string can be used with widget's `state <tkinter.ttk.Widget.state>`/`instate <tkinter.ttk.Widget.instate>` functions.
        '''
        for name, value in self.items():
            yield (name, value, GUI_STATES[name])


@dataclass
class GuiState_Tk:
    '''Information about ``Tk`` states.

    The states applied to the widgets are very confusing, so store all the
    necessary metadata here.

    See `GuiState`, `GUI_STATES`, `GUI_STATES_common`.

    Example:
        The examples will analyse `GUI_STATES`.

        The simplest example is the ``"readonly"`` element. The ``Tk`` string
        is ``readonly``, so ``invert`` is `False`, the semantic values match.

        On the other hand, for the ``"enabled"`` element, the ``Tk`` string is
        ``disabled``, so ``invert`` is `True`. The semantic values are
        inverted.
    '''

    string: str
    '''The ``Tk`` string used in the state-releated functions.'''
    invert: bool
    '''Is the ``string`` state the opposite from its sematic value?'''

    def gstr(self) -> str:
        '''Get the ``Tk`` string to obtain the value.

        This already takes into account the ``invert`` parameter.

        See the `instate <tkinter.ttk.Widget.instate>` function.
        '''
        if self.invert:
            return f'!{self.string}'
        else:
            return self.string


GUI_STATES: typing.Mapping[str, GuiState_Tk] = {
    'enabled': GuiState_Tk(tk.DISABLED, invert=True),
    'valid': GuiState_Tk('invalid', invert=True),
    'readonly': GuiState_Tk('readonly', invert=False),
}
'''`GuiState` ``Tk`` metadata.

See `GuiState_Tk`.'''

GUI_STATES_common = ('enabled', 'valid')
'''`GuiState` common to all widgets.

See `GUI_STATES`.'''
assert set(GUI_STATES.keys()) == set(f.name for f in fields(GuiState))
assert set(GUI_STATES_common) < set(f.name for f in fields(GuiState))


class MixinBinding:
    ''''''  # Internal, do not document
    _binding: typing.Callable

    def __init__(self, widget: 'mixin.MixinWidget', sequence: str, action: typing.Callable, *, immediate: bool = False, description: typing.Optional[str] = None):
        assert isinstance(widget, (tk.Widget, tk.Tk)), f'{widget} is not a valid widget'
        self.obj = None
        self.widget = widget
        self.sequence = sequence
        self.action = action
        self.description: str = description or f'Calling "{action.__name__}"'
        if immediate:
            self.enable()

    def __bool__(self):
        '''Check if the binding is enabled.

        Should be used as:

        .. code:: python

            if binding:
                print('Binding is enabled')
            else:
                print('Binding is disabled')
        '''
        return self.obj is not None

    def _bind(self) -> typing.Any:
        raise NotImplementedError

    def _unbind(self, obj: typing.Any) -> None:
        raise NotImplementedError

    def enable(self) -> None:
        '''Enable the binding.'''
        if self.obj is None:
            self.obj = self._bind()
        else:
            warnings.warn(f'Redundant enable @ {self!r}')

    def disable(self) -> None:
        '''Disable the binding.'''
        if self.obj is not None:
            obj = self.obj
            try:
                self.obj = None
                self._unbind(obj)
            except Exception as e:
                self.obj = obj  # Restore
                raise Exception(f'Error when unbinding @ {self.widget!r}') from e
        else:
            warnings.warn(f'Redundant disable @ {self!r}')


class Binding(MixinBinding):
    '''Wrap a stateful binding.

    Can be enabled and disabled separately from creation. Default to starting
    disabled. Note that this is the opposite from the actions of the wrapped
    functions.

    See Python documentation for `bindings and events <https://docs.python.org/3/library/tkinter.html#bindings-and-events>`_.

    ..
        Python 3.8 is missing this reference, included in Python 3.9:

        :ref:`bindings and events <python:Bindings-and-Events>`

    Args:
        widget: The widget to apply the binding to.
        sequence: The sequence to bind to. See ``Tk`` `bind
            <https://www.tcl.tk/man/tcl/TkCmd/bind.html>`_ documentation, not
            everything applies here.
        action: The function to call when the binding is hit.
        immediate: Enable binding on creation.
            Defaults to ``False``, requiring separate activation.
        description: Optional description of the binding action.
            Useful for debugging, not used for any purpose for now.

    Note:
        When the ``action`` function returns ``"break"``, no more actions are
        considered. Use this with care.

    See Also:
        For the global version of this, see `BindingGlobal`.

    .. automethod:: __bool__
    .. automethod:: enable
    .. automethod:: disable
    '''
    def __init__(self, widget: 'mixin.MixinWidget', sequence: str, *args, **kwargs):
        if sequence in widget.wroot._bindings_global:
            # Warn when widget bindings are aliased by global bindings
            warnings.warn(f'Global binding for "{sequence}" aliases {widget!r} binding')
            # Should this be an error?
        super().__init__(widget, sequence, *args, **kwargs)

    def _bind(self):
        return self.widget.bind(sequence=self.sequence, func=self.action, add=True)

    def _unbind(self, obj):
        self.widget.unbind(self.sequence, obj)

    def __repr__(self) -> str:
        return f'Binding("{self.sequence}" @ {self.widget})  # {self.description}'


class BindingGlobal(MixinBinding):
    '''Wrap a stateful global binding.

    This is a global version of the `Binding` object. The main difference is
    that the ``widget`` argument is ignored, the binding applies to the entire
    application (technically, the widget's `mixin.MixinWidget.wroot` (a
    `RootWindow`).

    The `RootWindow` will store a dictionary of sequences to `BindingGlobal`.
    This is similar to `mixin.MixinWidget.binding`.

    Args:
        widget: The widget to apply the binding to. This can be any widget,
            only the corresponding `RootWindow` is considered.
        sequence: The sequence to bind to. See ``Tk`` `bind
            <https://www.tcl.tk/man/tcl/TkCmd/bind.html>`_ documentation, not
            everything applies here.
        action: The function to call when the binding is hit.
        immediate: Enable binding on creation.
            Defaults to ``False``, requiring separate activation.
        description: Optional description of the binding action.
            Useful for debugging, not used for any purpose for now.

    Note:
        When the ``action`` function returns ``"break"``, no more actions are
        considered. Use this with care.

    See Also:
        For the widget version of this, see `Binding`.

    .. automethod:: __bool__
    .. automethod:: enable
    .. automethod:: disable
    '''
    def __init__(self, widget: 'mixin.MixinWidget', sequence: str, *args, **kwargs):
        root_widget = widget.wroot
        if sequence in root_widget._bindings_global:
            raise ValueError(f'Repeated global binding for "{sequence}"')
        super().__init__(root_widget, sequence, *args, **kwargs)
        # Store all global bindings
        root_widget._bindings_global[sequence] = self

    def _bind(self):
        return self.widget.bind_all(sequence=self.sequence, func=self.action, add=True)

    def _unbind(self, obj):
        self.widget.unbind(self.sequence, obj)

    def __repr__(self) -> str:
        return f'BindingGlobal("{self.sequence}")  # {self.description}'


class BindingTag(MixinBinding):
    '''Wrap a stateful tag binding for `EntryMultiline`.

    This is a version of the `Binding` object which applies only to the tags in
    `EntryMultiline`.

    Args:
        widget: The widget to apply the binding to. This can be any widget,
            only the corresponding `RootWindow` is considered.
        tag: The sub-widget tag where the binding applies.
        sequence: The sequence to bind to. See ``Tk`` `bind
            <https://www.tcl.tk/man/tcl/TkCmd/bind.html>`_ documentation, not
            everything applies here.
        action: The function to call when the binding is hit.
        immediate: Enable binding on creation.
            Defaults to ``False``, requiring separate activation.
        description: Optional description of the binding action.
            Useful for debugging, not used for any purpose for now.

    Note:
        When the ``action`` function returns ``"break"``, no more actions are
        considered. Use this with care.

    .. automethod:: __bool__
    .. automethod:: enable
    .. automethod:: disable
    '''
    def __init__(self, widget: 'EntryMultiline', tag: str, sequence: str, *args, **kwargs):
        self.tag = tag
        if sequence in widget.wroot._bindings_global:
            # Warn when widget bindings are aliased by global bindings
            warnings.warn(f'Global binding for "{sequence}" aliases {widget!r}(tag "{tag}") binding')
            # Should this be an error?
        super().__init__(widget, sequence, *args, **kwargs)

    def _bind(self):
        return self.widget.tag_bind(tagName=self.tag, sequence=self.sequence, func=self.action, add=True)

    def _unbind(self, obj):
        self.widget.tag_unbind(self.tag, self.sequence, obj)

    def __repr__(self) -> str:
        return f'BindingTag("{self.sequence}" @ {self.widget}|{self.tag})  # {self.description}'


class Timeout:
    '''Schedule an action into the future time, cancellable.

    The ``timeout`` argument (also in `schedule`) acts as a deadline, after
    which the ``action`` is invoked.

    Can be scheduled and unscheduled separately from creation, see the
    ``immediate`` argument.

    See ``tcl`` `after <https://www.tcl.tk/man/tcl/TclCmd/after.html>`_ documentation.

    Args:
        widget: The widget to apply the timeout to. When in doubt, use the
            `wroot <mixin.MixinWidget.wroot>` widget.
        action: The function to call when the timeout expires.
        timeout: The expiration time for the timeout, in milliseconds.
            This only starts to count from the scheduling time, not the object
            creation, but see ``immediate``.
        immediate: Schedule timeout on creation.
            Defaults to `True`, set to `False` to schedule separately.

    See Also:
        For the idling version of this, see `TimeoutIdle`.
    '''
    _obj: typing.Union[None, str, typing.Literal[False]]
    # _obj States:
    # - None: Unscheduled. The default
    # - str: Scheduled, this is the id for `after_cancel`
    # - False: Unscheduled, since it was already triggered.
    # Note the truthy value is enough to know if this is scheduled
    # Get information with `self.widget.tk.call('after', 'info', self._obj)`

    def __init__(self, widget: 'mixin.MixinWidget', action: typing.Callable, timeout: int, immediate: bool = True):
        self._obj = None
        self.widget = widget
        self.action = action
        self.timeout = timeout
        if immediate:
            self.schedule()

    def isScheduled(self) -> bool:
        '''Check if the timeout is scheduled to run in the future.

        This is `True` after calling `schedule`, and before the action runs.
        '''
        return bool(self._obj)

    def isTriggered(self) -> bool:
        '''Check if the timeout has been triggered yet.

        This is `True` just before the action runs. Note that `isScheduled`
        will return `False` in this case.
        '''
        return self._obj is False

    def _action(self, *args, **kwargs) -> None:
        '''Run the saved action, and setup the `isTriggered` flag.'''
        assert self.isScheduled(), f'{self}: Invalid action @ {self._obj!r}'
        # Memory leak, save the old `_obj`? `after_cancel` it?
        self._obj = False  # Mark as triggered
        self.action(*args, **kwargs)

    def schedule(self, _e: typing.Any = None, *, timeout: typing.Optional[int] = None) -> None:
        '''Schedule the timeout to run in the future.

        This tries to unschedule the timeout, and schedules it again, to avoid
        possible race conditions.
        The countdown for the expiration in ``timeout`` milliseconds starts when this function is called.

        Note the override values only take effect in this particular call, they
        are not permanent changes.

        Args:
            timeout: Override the timeout to consider on the next call.

            _e: Unused, included for API compatibility with ``Tk`` events
        '''
        assert isinstance(self.widget, (tk.Widget, tk.Tk)), f'{self} is not a valid widget'
        self.unschedule()  # Try to unschedule first
        self._obj = self.widget.after(
            ms=timeout or self.timeout,
            func=self._action
        )
        assert bool(self._obj), f'Invalid ID: {self._obj!r}'

    def unschedule(self, _e: typing.Any = None) -> None:
        '''Cancel the timeout.

        Args:
            _e: Unused, included for API compatibility with ``Tk`` events
        '''
        assert isinstance(self.widget, (tk.Widget, tk.Tk)), f'{self} is not a valid widget'
        obj = self._obj
        if obj:
            # Can this fail?
            # Possible race with `_action`
            self.widget.after_cancel(obj)
            self._obj = None

    # Alias scheduling function
    reschedule = schedule
    '''Reschedule the timeout (alias for `schedule`).'''

    def toggle(self, _e: typing.Any = None) -> bool:
        '''Toggle the schedule state.

        Args:
            _e: Unused, included for API compatibility with ``Tk`` events

        Returns:
            Return the new state, equivalent to calling `isScheduled` right afterwards.
        '''
        if self.isScheduled():
            self.unschedule()
            return False
        else:
            self.schedule()
            return True


class TimeoutIdle:
    '''Schedule an action into the future, whenever there's nothing else to do.

    This adds an idle task to the ``tk`` event loop, to be invoked when there's
    no other action to take. This is very useful to push actions to the future,
    but not block the UI thread.

    Can be scheduled and unscheduled separately from creation, see the
    ``immediate`` argument.

    See ``tcl`` `after idle <https://www.tcl.tk/man/tcl/TclCmd/after.html#M9>`_ documentation.

    Args:
        widget: The widget to apply the timeout to. When in doubt, use the
            `wroot <mixin.MixinWidget.wroot>` widget.
        action: The function to call when the application goes idle.
        immediate: Schedule timeout on creation.
            Defaults to `True`, set to `False` to schedule separately.

    See Also:
        For a version of this that specifies a deadline, see `Timeout`.
    '''
    _obj: typing.Union[None, str, typing.Literal[False]]
    # _obj States:
    # - None: Unscheduled. The default
    # - str: Scheduled, this is the id for `after_cancel`
    # - False: Unscheduled, since it was already triggered.
    # Note the truthy value is enough to know if this is scheduled
    # Get information with `self.widget.tk.call('after', 'info', self._obj)`

    def __init__(self, widget: 'mixin.MixinWidget', action: typing.Callable, immediate: bool = True):
        self._obj = None
        self.widget = widget
        self.action = action
        if immediate:
            self.schedule()

    def isScheduled(self) -> bool:
        '''Check if the timeout is scheduled to run in the future.

        This is `True` after calling `schedule`, and before the action runs.
        '''
        return bool(self._obj)

    def isTriggered(self) -> bool:
        '''Check if the timeout has been triggered yet.

        This is `True` after the action runs. Note that `isScheduled` will
        return `False` in this case.

        Note:
            During the action function call, this is `False`, and it will
            never be `True` if it calls `reschedule` inside the action.
        '''
        return self._obj is False

    def _action(self, *args, **kwargs) -> None:
        '''Run the saved action, and setup the `isTriggered` flag.'''
        assert self.isScheduled(), f'{self}: Invalid action @ {self._obj!r}'
        self._obj = False  # Mark as triggered
        # TODO: Use `try`/`catch`? Not used on the `after_idle` function
        self.action(*args, **kwargs)

    def schedule(self, _e: typing.Any = None) -> None:
        '''Schedule the timeout to run in the future.

        This tries to unschedule the timeout, and schedules it again, to avoid
        possible race conditions.
        The action is added to the event loop when this function is called.

        When called for an already scheduled object, this is equivalent to
        moving the action back to the end of the queue.

        Args:
            _e: Unused, included for API compatibility with ``Tk`` events
        '''
        assert isinstance(self.widget, (tk.Widget, tk.Tk)), f'{self} is not a valid widget'
        self.unschedule()  # Try to unschedule first
        # TODO: Track the scheduled time and provide an absolute timeout?
        #       This is only to avoid infinite loops
        self._obj = self.widget.after_idle(
            func=self._action
        )
        assert bool(self._obj), f'Invalid ID: {self._obj!r}'

    def unschedule(self, _e: typing.Any = None) -> None:
        '''Cancel the timeout.

        This removes the action from the event loop.

        Args:
            _e: Unused, included for API compatibility with ``Tk`` events
        '''
        assert isinstance(self.widget, (tk.Widget, tk.Tk)), f'{self} is not a valid widget'
        obj = self._obj
        if obj:
            # Can this fail?
            # Possible race with `_action`
            self.widget.after_cancel(obj)
            self._obj = None

    # Alias scheduling function
    reschedule = schedule
    '''Reschedule the timeout (alias for `schedule`).'''

    def toggle(self, _e: typing.Any = None) -> bool:
        '''Toggle the schedule state.

        Args:
            _e: Unused, included for API compatibility with ``Tk`` events

        Returns:
            Return the new state, equivalent to calling `isScheduled` right afterwards.
        '''
        if self.isScheduled():
            self.unschedule()
            return False
        else:
            self.schedule()
            return True


@dataclass
class NotebookTab:
    '''Information for each `Notebook <tkmilan.Notebook>` tab.

    These are the parameters which can be configured:

    Args:
        name: The visible text on the tab itself
        widget: The widget corresponding to the tab. Must be a `container <mixin.ContainerWidget>`.
        image: Show an icon on the tab. Optional.
        extra:
            more arguments to the `add <tkinter.ttk.Notebook.add>` function. This
            is an escape hatch, optional.
        labelPosition:
            When the "image" is set, adjust the label position. When set to
            `CP.default`, only the image is included and no label is shown.

            Defaults to ``CP.E``, not available on the object.

    There are other parameters which are automatically calculated:

    Parameters:
        identifier: The internal tab identifier. Set by the widget itself.
        imageCompound: The ``compound`` settings. Based on "labelPosition",
            automatically calculated.

    Note:
        Technically, it is possible to have `single widgets <mixin.SingleWidget>` as "widget",
        but this results in broken layouts.
    '''
    name: str
    widget: 'mixin.ContainerWidget'
    image: typing.Optional[tk.Image] = None
    extra: typing.Mapping[str, typing.Any] = dc_field(default_factory=dict)
    labelPosition: InitVar[CP] = CP.E  # init-only
    identifier: typing.Optional[str] = dc_field(default=None, init=False)
    imageCompound: str = dc_field(init=False)

    def __post_init__(self, labelPosition: CP):
        if self.image:
            if labelPosition not in CP_Compound:
                raise ValueError(f'Invalid CP for "compound": {labelPosition}')
            self.imageCompound = CP_Compound[labelPosition]
        else:
            self.imageCompound = CP_Compound[False]


@dataclass
class TreeColumn:
    '''Information for each `tkmilan.Tree` column heading.

    Args:
        identifier: The id string. This is not shown to the user
        name: The heading name, shown on the top of the column
    '''
    identifier: str
    name: str
    # TODO: image
    # TODO: anchor: CP


@dataclass
class TreeElement:
    '''Information for each `tkmilan.Tree` record.

    Technically, this is not enough to reconstruct the entire tree, but it
    should.

    The ``image`` argument is optional, but when created, no resizing is performed.
    By default, the ideal image size is ``16x16`` pixels.

    Args:
        label: The leftmost string shown on the first column. This identifies the entire record.
        columns: A list of strings corresponding to the column data.
            Optional, defaults to `None`.
        children: A list of `TreeElement`, to be shown as children of this
            `TreeElement`. This can recurse without limit.
            Optional, defaults to `None`.
        image: Show an icon on the left side of the record. Optional.
        data: Arbitrary data to store on the element.
            Optional, defaults to `None`.
    '''
    label: str
    columns: typing.Optional[typing.Sequence[str]] = None
    children: 'typing.Optional[typing.Sequence[TreeElement]]' = None
    image: typing.Optional[tk.Image] = None
    data: typing.Any = None


class TextElement(abc.ABC):
    '''Common text element class.

    This is only an abstract class, a common base class for all the possible
    text elements.
    '''
    text: str
    atags: typing.Sequence[str]


@dataclass
class TextElementInline(TextElement):
    '''Text Element: A inline text span, with optional tags.

    This is the most basic text element, just some inline string.
    It can optionally define one main tag, and other secondary tags to apply to
    the text.

    Args:
        text: The string of text. Mandatory
        tag: The main tag for the text. Optional.
        tags: A list of secondary tags. Optional.
        data: A dictionary of ``data-*`` attributes. Default to an empty dictionary.

    Note:
        Setting secondary tags without a main tag is invalid.
    '''
    text: str
    tag: typing.Optional[str] = None
    tags: typing.Optional[typing.Sequence[str]] = None
    data: typing.Mapping[str, str] = dc_field(default_factory=dict)  # TODO: Default to `None`?

    def __post_init__(self):
        if self.tag is not None:
            if self.tags is not None:
                if self.tag in self.tags:
                    raise ValueError(f'Invalid tag complex: {self.tag} @ {self.tags}')
        else:
            assert self.tags is None, 'Secondary tags without main tag'
        if '\n' in self.text:
            tag_name = 'text' if self.tag is None else f'<{self.tag}>'
            warnings.warn(f'{tag_name} should not have newlines, use <br/>', stacklevel=14)
        self.has_tags = True

    @property
    def atags(self):
        '''Get all tags defined in the element.'''
        atags = []
        if self.tag:
            atags.append(self.tag)
        if self.tags:
            atags.extend(self.tags)
        return tuple(atags)


@dataclass
class TextElement_br(TextElement):
    '''Text Element: Line break.

    This is equivalent to a `TextElementInline` with ``"\\n"`` as text.
    '''
    def __post_init__(self):
        self.text = '\n'
        self.atags = tuple()
