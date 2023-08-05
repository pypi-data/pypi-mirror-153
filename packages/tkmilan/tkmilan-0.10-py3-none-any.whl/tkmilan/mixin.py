'''
All the mixin classes, to be reused internally
'''
import logging
import warnings
import typing
from dataclasses import dataclass
import collections
from functools import cached_property, partial

from . import fn
from . import model
from . import var
from . import autolayout

import tkinter as tk

if typing.TYPE_CHECKING:
    from . import RootWindow, ScrolledWidget

logger = logging.getLogger(__name__)

WEIRD_WIDGET_NAME = [  # Weird Widget `dir` names, these cause trouble
    '_last_child_ids',
    'wroot',
]


# Technically a model, but internal
@dataclass
class ContainerState:
    '''Full container state.

    Args:
        swidgets: Single Widgets
        cwidgets: Container Widgets
        variables: Attached Variables
        wvariables: Mapping VariableID -> Variable object
        vwidgets: Mapping VariableID -> Widget Name list
        vid_upstream: Set of upstream VariableID
    '''
    swidgets: 'typing.Mapping[str, SingleWidget]'
    cwidgets: 'typing.Mapping[str, ContainerWidget]'
    variables: 'typing.Mapping[str, var.Variable]'
    wvariables: 'typing.Mapping[str, var.Variable]'
    vwidgets: typing.Mapping[str, typing.Iterable[str]]
    vid_upstream: typing.Set[str]


class MixinState:
    '''Mixin for all stateful widgets.'''

    wstate_static: bool = True
    '''
    Define if the `setup_state` cache is static. or a callable for dynamic
    calculations.

    See `stateSetup`.
    '''

    isNoneable: typing.Optional[bool] = None
    '''Define if a `None` result leads to skipping this widget on the state result.

    This applies to both static and dynamic state calculations. Defaults to
    `None`, so that it can be overriden by subclasses.

    For dynamic calculations, the results for some widgets might vary depending
    on where the root state starts, so they will be unpredictable. When the
    state is taken as a whole (the simple usage), it is predictable.

    Note:
        The default `None` value for this variable is invalid. The subclass
        **must** define this.
    '''

    def setup_state(self):
        '''Define an object that will be cached forever.

        This can have a static object, or a dynamic `callable`.

        See `wstate_static`, `stateSetup`.
        '''
        raise NotImplementedError

    @cached_property
    def stateSetup(self):
        '''Obtain the state setup.

        This takes into account the `wstate_static` flag, producing a static object
        or a callable.

        This should always be used, `setup_state` is only a definition.
        '''
        assert self.isNoneable is not None, f'{self} needs `isNoneable` choice'
        if self.wstate_static is True:
            return self.setup_state()
        else:
            return self.setup_state

    def state_get(self, *args, **kwargs):
        '''Define how to get the widget state.

        The kwargs are only passed for Dynamic State widgets
        '''
        raise NotImplementedError

    '''
    Define how to set the widget state.

    The kwargs are only passed for Dynamic State widgets
    '''
    def state_set(self, state, substate: bool, **kwargs):
        raise NotImplementedError

    # Wrapper functions for the property
    def wstate_get(self, *args, **kwargs):
        return self.state_get(*args, **kwargs)

    def wstate_set(self, state, *args, substate=False, **kwargs):
        return self.state_set(state, *args, substate=substate, **kwargs)

    wstate = property(wstate_get, wstate_set, doc='Widget State')


class MixinStateSingle(MixinState):
    '''
    Mixin class for single widgets.

    Note:
        When subclassing this, define `MixinState.setup_state` to return the
        variable containing the widget state.
    '''
    wstate_static: bool = True

    def state_get(self):
        return self.stateSetup.get()

    def state_set(self, state, substate):
        if __debug__:
            if substate is True:  # Just skip it silently?
                warnings.warn("`substate` doesn't apply here", stacklevel=3)
        self.stateSetup.set(state)


class MixinStateContainer(MixinState):
    '''Mixin class for container widgets.

    Note:
        When subclassing this, define `MixinState.setup_state` to return a
        dictionary mapping subwidget identifier to `WidgetDynamicState`.
    '''
    wstate_static: bool = False
    wstate_single: typing.Optional[str] = None
    '''
    Mark the container state as "single", including only the state for this child.

    Should only be enabled where there is a single child element, this is
    verified when getting the value. Use `MixinWidget.ignoreContainerState` to
    ignore other widgets.

    This creates no performance improvements, it is only useful to simplify the
    state.
    '''

    def state_get(self, **kwargs):
        state = {}
        for identifier, wds in self.stateSetup(**kwargs).items():
            result = wds.getter()
            if wds.noneable and result is None:
                pass  # Skip
            else:
                state[identifier] = result
        if self.wstate_single is not None:
            assert len(state) == 1, f'{self}: Invalid "wstate_single" marking, {len(state)} elements'
            return state[self.wstate_single]
        else:
            if len(state) == 0:
                return None
            else:
                if __debug__:
                    if len(state) == 1:
                        logger.warning('%s: This widget can be marked "wstate_single": `%s`', self, list(state)[0])
                return state

    def state_set(self, state, substate, **kwargs) -> None:
        # # Debug container state flow
        # self_names = None
        # if __debug__:
        #     self_names = str(self).split('.')[1:]
        #     logger.debug('%s: %s%s',
        #                  '>' * len(self_names),
        #                  self,
        #                  '' if self.wstate_single is None else f' [{self.wstate_single}]',
        #                  )
        for identifier, wds in self.stateSetup(**kwargs).items():
            skip = (wds.noneable and state is None) or \
                ((substate or wds.noneable) and identifier not in state) or \
                (self.wstate_single is not None and self.wstate_single != identifier)
            if skip:
                # if __debug__:
                #     logger.debug('%s|> Skip "%s"', ' ' * len(self_names), identifier)
                pass
            else:
                # if __debug__:
                #     logger.debug('%s|>  Set "%s"', ' ' * len(self_names), identifier)
                if self.wstate_single:
                    widget_state = state
                else:
                    widget_state = state[identifier]
                if wds.container:
                    wds.setter(widget_state, substate, **kwargs)
                else:
                    wds.setter(widget_state)


class MixinWidget:
    '''Parent class of all widgets.

    Args:
        gkeys: Append widget-specific `GuiState` keys to common list
            `model.GUI_STATES_common`.

    .. autoattribute:: _bindings
    .. autoattribute:: _tidles
    '''

    wparent: 'typing.Optional[MixinWidget]' = None
    '''A reference to the parent widget.'''
    gkeys: typing.FrozenSet[str]
    '''The supported `GuiState` keys.'''
    isHelper: bool
    '''Marker that indicates the widgets is not part of the automatic state.'''
    ignoreContainerState: bool = False
    '''Ignore this widget's state when included on a container.'''
    _bindings: typing.MutableMapping[str, model.Binding]
    '''Store all widget `Binding` objects, keyed by name (see `binding`).'''
    _tidles: typing.MutableMapping[str, model.TimeoutIdle]
    '''Store some widget `TimeoutIdle` objects, keyed by name (see `tidle`).'''

    def __init__(self, *, gkeys: typing.Iterable[str] = None):
        self.isHelper: bool = getattr(self, 'isHelper', False)
        self._bindings = {}
        self._tidles = {}
        gk = set(model.GUI_STATES_common)
        if gkeys:
            gk.update(gkeys)
        self.gkeys = frozenset(gk)

    @cached_property
    def wroot(self) -> 'RootWindow':
        '''Get the root widget, directly.

        Does not use the ``wparent`` property to crawl the widget tree to the
        top, so that it might be called before that setup is done (during setup
        of lower widgets, for example).
        '''
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid widget'
        widget = self.nametowidget('.')
        if __debug__:
            from . import RootWindow  # For typechecking
        assert isinstance(widget, RootWindow)
        return widget

    def wroot_search(self) -> 'RootWindow':
        '''Alternative to `wroot` that crawls the widget tree.

        Use the `wparent` proprety.

        See Also:
            `wroot`: Simpler alternative to this function, crawling the widget
            tree. Requires all widgets to be stable.
        '''
        if self.wparent is None:
            # This might be triggered if called before all widgets are stable
            if __debug__:
                from . import RootWindow  # For typechecking
            assert isinstance(self, RootWindow), f'Invalid "root" widget: {self!r}'
            return self
        else:
            return self.wparent.wroot_search()

    def binding(self, sequence: str, *args, key: str = None, immediate: bool = True, **kwargs) -> model.Binding:
        '''Create a `model.Binding` for this widget.

        Stores all widget bindings on a per-instance dictionary, for later
        usage. Note that all dictionary keys must be different. For the same
        bindings on a single widget, this requires passing the ``key``
        argument.

        See the ``Tk`` `bind <https://www.tcl.tk/man/tcl/TkCmd/bind.html>`_ documentation.

        Args:
            key: Optional. Defaults to the ``sequence`` itself. Useful to
                support multiple bindings on the same sequence.
            immediate: Passed to the upstream object, default to enabling the
                binding on creation. This is the opposite from upstream.

        All other arguments are passed to the `model.Binding` object.
        '''
        name = key or sequence
        if name in self._bindings:
            raise ValueError(f'Repeated Binding for "{sequence}" in {self!r}. Change the "key" parameter.')
        self._bindings[name] = model.Binding(self, sequence, *args, immediate=immediate, **kwargs)
        return self._bindings[name]

    def tidle(self, action: typing.Callable, *args, key: str = None, **kwargs) -> model.TimeoutIdle:
        '''Create a `model.TimeoutIdle` for this widget.

        Stores all idle timeouts created using this function on a per-instance
        dictionary, for later usage. If the ``action`` is not a "real"
        function, this requires passing the ``key`` argument.

        Args:
            key: Optional. Defaults to the ``action`` name.

        All other arguments are passed to `model.Binding` object.
        '''
        name = key or action.__name__
        if name in self._tidles:
            raise ValueError(f'Repeated TimeoutIdle for "{name}" in {self!r}.')
        self._tidles[name] = model.TimeoutIdle(self, action, *args, *kwargs)
        return self._tidles[name]

    @property
    def size_vroot(self) -> 'model.PixelSize':
        '''The VirtualRoot size.

        This is a global property, but it's available in every widget.
        '''
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid tkinter.Widget'
        return model.PixelSize(
            width=self.winfo_vrootwidth(),
            height=self.winfo_vrootheight(),
        )

    @property
    def size_screen(self) -> 'model.PixelSize':
        '''The screen size.

        This is a global property, but it's available in every widget.
        '''
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid tkinter.Widget'
        return model.PixelSize(
            width=self.winfo_screenwidth(),
            height=self.winfo_screenheight(),
        )

    def setup_grid(self, fmt: typing.Union[str, model.GridCoordinates], **kwargs) -> None:
        '''Configure the grid for the current widget.

        ``fmt`` can be given as a `model.GridCoordinates`, or as a single
        `str`, to be parsed by `model.GridCoordinates.parse`.

        Args:
            fmt: The grid configuration format. Specified above.
            kwargs: Passed upstream

        See Also:
            `wgrid`: Get the current widget grid coordinates.
        '''
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid tkinter.Widget'
        if isinstance(fmt, str):
            fmt = model.GridCoordinates.parse(fmt)
        kwargs.update(fmt.dict())
        self.grid(**kwargs)

    @property
    def wgrid(self) -> typing.Optional[model.GridCoordinates]:
        '''Get the widget grid coordinates, if the widget is visible.

        Returns:
            Return a `model.GridCoordinates` object with the widget information. If
            the wiget was hidden, return `None`.

            This is also available for the root widget (`wroot`) for
            completeness, but that doesn't really correspond to any grid,
            return `None`.

        See Also:
            `setup_grid`: Change the widget grid coordinates.
        '''
        if self == self.wroot:
            assert isinstance(self, tk.Tk)
            return None
        else:
            assert isinstance(self, tk.Widget), f'{self} is not a valid tkinter.Widget'
            # If the grid information doesn't exist, default to a single frame
            # Force elements to integer, on tcl v8.5 they are returned as strings
            ginfo = self.grid_info()
            if ginfo:
                return model.GridCoordinates(
                    row=int(ginfo.get('row', 0)),
                    rowspan=int(ginfo.get('rowspan', 1)),
                    column=int(ginfo.get('column', 0)),
                    columnspan=int(ginfo.get('columnspan', 1)),
                )
            else:
                return None

    def get_gui_state(self) -> model.GuiState:
        if __debug__:
            from . import RootWindow  # For typechecking
        assert isinstance(self, (tk.ttk.Widget, RootWindow)), f'{self} is not a valid tkinter.ttk.Widget'
        state: typing.MutableMapping[str, typing.Optional[bool]] = {}
        for estr in self.gkeys:
            itk = model.GUI_STATES[estr]
            state[estr] = self.instate([itk.gstr()])
            # logger.debug('  [%s] » %s', itk.gstr(), state[estr])
        rval = model.GuiState(**state)
        # if __debug__:
        #     logger.debug('State > %r', rval)
        return rval

    def set_gui_state(self, state: typing.Optional[model.GuiState] = None, **kwargs) -> None:
        assert isinstance(self, tk.ttk.Widget), f'{self} is not a valid tkinter.ttk.Widget'
        if state is None:
            state = model.GuiState(**kwargs)
        states = []
        # if __debug__:
        #     logger.debug('State < %r', state)
        for estr, sval, itk in state.items_tk():
            if sval is not None:
                assert estr in self.gkeys, f'{self.__class__.__name__}| Invalid GuiState: {estr}'
                # Invert `sval` when `itk.invert` == `sval XOR itk.invert`
                if sval is not itk.invert:
                    tkstr = '%s' % itk.string
                else:
                    tkstr = '!%s' % itk.string
                # logger.debug('  [%s %s] » %s', sval, itk.invert, tkstr)
                states.append(tkstr)
        self.state(states)

    # Wrapper functions for the property
    def gstate_get(self):
        return self.get_gui_state()

    def gstate_set(self, state: model.GuiState):
        return self.set_gui_state(state)

    # TODO: This can be even better
    # Support `widget.gstate.enabled = NEW_VALUE`
    # Not a property, but a class that changes `self`
    gstate = property(gstate_get, gstate_set, doc='GUI State')


class MixinTraces:
    def init_traces(self):
        self._traces: typing.MutableMapping[str, str] = {}
        assert self.variable is not None, f'{self}: Widget untraceable'

    def trace(self, function: typing.Callable, *, trace_mode: model.TraceModeT = 'write', trace_name: typing.Optional[str] = None, **kwargs: typing.Any) -> str:
        assert isinstance(self, SingleWidget), f'{self.__class__.__name__}: Unsupported tracing for this Widget'
        assert self.variable is not None, f'{self}: Widget untraceable'
        function_name = self.variable.trace_add(
            trace_mode,
            fn.generate_trace(
                self.variable,
                function,
                **kwargs,
            ),
        )
        key = trace_name or function_name
        assert key not in self._traces, f'{self}: Repeated trace name: {key}'
        self._traces[key] = function_name
        return function_name


# High-Level Mixins


class SingleWidget(MixinWidget, MixinStateSingle, MixinTraces):
    '''Parent class of all single widgets.'''
    variable: typing.Optional[var.Variable] = None
    state_type: typing.Optional[typing.Type[var.Variable]] = None
    scrollFrame: 'typing.Optional[ScrolledWidget]' = None
    '''Link to the corresponding `ScrolledWidget`, if exists'''

    def init_single(self, variable: var.Variable = None, gkeys: typing.Iterable[str] = None) -> None:
        '''Setup all single widget stuff.'''
        MixinWidget.__init__(self, gkeys=gkeys)
        self.variable = self.setup_variable(variable)
        MixinTraces.init_traces(self)
        if self.isNoneable is None:
            # Calculate isNoneable option
            self.isNoneable = self.state_type is var.nothing

    def setup_variable(self, variable: typing.Optional[var.Variable]) -> var.Variable:
        assert self.state_type is not None
        if variable is None:
            variable = self.state_type()
        assert isinstance(variable, self.state_type), f'Incompatible variable type ({type(variable).__name__}/{self.state_type.__name__})'
        return variable

    def setup_state(self):
        return self.variable

    def wimage(self, key: str) -> typing.Optional[tk.Image]:
        '''Wraper for `RootWindow.wimage`.'''
        return self.wroot.wimage(key)

    # TODO: Move here from Combobox
    # specValues: typing.Optional[spec.Spec]
    # def setDefault(self) -> None:
    #     if self.specValues:
    #         self.wstate = self.specValues.default
    #
    # def eSet(self, value: typing.Any) -> typing.Callable[..., None]:
    #    ...  # To Be overriden


# TODO: Support MixinTraces? Synthetic trace of all sub widgets?
class ContainerWidget(MixinWidget, MixinStateContainer):
    '''Parent class of all containers.'''
    layout: typing.Optional[str] = ''  # Automatic AUTO

    def init_container(self, *args, layout: typing.Optional[str] = '', expand: bool = True, autogrow: bool = True, **kwargs):
        '''
        Setup all the container stuff
        '''
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid tkinter.Widget'
        MixinWidget.__init__(self)
        self._variables: typing.MutableMapping[str, tk.Variable] = {}  # Allow attaching variables to containers
        # Calculate child widgets
        _existing_names = set(dir(self))
        _existing_ids = None
        if __debug__:
            _existing_ids = {
                name: id(self.__dict__.get(name, None))
                for name in _existing_names
                if name not in WEIRD_WIDGET_NAME
            }
        widgets = self.setup_widgets(*args, **kwargs)
        if __debug__:
            assert _existing_ids is not None
            overriden_names = [name for name, eid in _existing_ids.items() if id(self.__dict__.get(name, None)) != eid]
            assert len(overriden_names) == 0, f'{self}: Overriden Names: {" ".join(overriden_names)}'
        _new_names = set(dir(self)) - _existing_names
        if widgets is None:
            children = [w for _, w in self.children.items()]
            # logger.debug('tk C: %r', self.children)
            widgets = {}
            dir_names = {id(getattr(self, name, None)): name for name in _new_names}
            for widget in children:
                assert isinstance(widget, MixinWidget), '{widget} is not a valid tkmilan widget'
                if not widget.isHelper:
                    wid = id(widget)
                    assert wid in dir_names, f'{self}: Missing "{widget}"[{widget!r}]'
                    name = dir_names[wid]
                    widgets[name] = widget
        # logger.debug('Widgets: %r', widgets)
        self.widgets: typing.Mapping[str, MixinWidget] = widgets
        for w in self.widgets.values():
            w.wparent = self
        if self.isNoneable is None:
            # Calculate isNoneable option: containers are always noneable
            self.isNoneable = True

        if layout is None or self.layout is None:
            # Allow for explicit `None` layouts
            chosen_layout = None
        elif layout != '':
            # Use the per-instance setting
            chosen_layout = layout
        elif self.layout != '':
            # Use the class setting
            chosen_layout = self.layout
        else:
            # Fallback
            chosen_layout = autolayout.AUTO
        self.layout_container(chosen_layout, expand, autogrow)
        self.setup_defaults()
        self.after_idle(lambda: self.setup_adefaults())  # No need for a `TimeoutIdle` here
        assert hasattr(self, 'grid'), f'{self!r} should have a grid method'
        if __debug__:
            aliases = set(self._variables.keys()).intersection(set(self.widgets.keys()))
            assert len(aliases) == 0, f'{self!r}: Aliased var/widgets: {" ".join(aliases)}'

    def setup_widgets(self, *args, **kwargs) -> typing.Optional[typing.Mapping[str, MixinWidget]]:
        '''Define the sub widgets here.

        Return a :py:class:`dict` for a custom mapping, or `None` for automatic mapping.
        '''
        raise NotImplementedError

    def var(self, cls: typing.Type[var.Variable], *, value=None, name=None) -> tk.Variable:
        '''"Attach" a new variable to this container.

        Args:
            cls: The variable class.

            value: The default value.
                Optional, defaults to `None`.
            name: The variable name.
                Optional, defaults to an autogenerated name.

        See Also:
            gvar: Access the variable by name.
        '''
        vobj = cls(value=value)
        assert isinstance(vobj, var.Variable), f'Class "{cls}" is not a "tk.Variable"'
        # Save the variables on the instance object
        self._variables[name or str(vobj)] = vobj
        return vobj

    def gvar(self, name: str):
        '''Get a variable attached to this container, by name.

        Fails if it does not exist.

        Args:
            name: The variable name to search for.

        See Also:
            var: Attach a variable to this container, with a name.
        '''
        return self._variables[name]

    def layout_container(self, layout: typing.Optional[str], expand: bool, autogrow: bool):
        assert isinstance(self, (tk.Widget, tk.Tk)), f'{self} is not a valid tkinter.Widget'
        if expand:
            assert isinstance(self, tk.ttk.Widget), f'{self} is not a valid tkinter.ttk.Widget'
            self.grid(sticky=tk.NSEW)
        # Automatic Layout
        layout, args = autolayout.do(layout, len(self.widgets))
        if layout:
            if __debug__:
                logger.debug(f'{self}: => {len(self.widgets)} widgets')
            for idx, (arg, widget) in enumerate(zip(args, self.widgets.values())):
                assert isinstance(widget, tk.Widget)
                widget.grid(**arg.dict())
        # TODO: Return a boolean/dataclass to control autogrowth
        self.setup_layout(layout)
        self.layout = layout  # Setup the final layout setting
        if autogrow:
            if size := self.gsize:
                fn.configure_grid(self, [1] * size.columns, [1] * size.rows)

    @property
    def gsize(self) -> model.GridSize:
        '''GUI grid size (according to the current child widgets).'''
        return fn.grid_size(*self.widgets.values())

    def state_c(self, *, vid_upstream: typing.Optional[typing.Set[str]] = None) -> ContainerState:
        swidgets = {}
        cwidgets = {}
        wvariables = {}
        vid_upstream = set(vid_upstream or ())
        vid_variables = set(fn.vname(v) for v in self._variables.values())
        vwidgets = collections.defaultdict(lambda: [])
        # logger.debug('%r START | %r', self, vid_upstream)
        for name, widget in self.widgets.items():
            # logger.debug('%s: %r', name, widget)
            if widget.ignoreContainerState:
                # logger.debug('| Skipping Widget')
                continue
            if isinstance(widget, SingleWidget):
                assert widget.variable is not None
                vid = fn.vname(widget.variable)
                # logger.debug('| Variable: %s[%r]', vid, widget.variable)
                if vid in vid_upstream:
                    # logger.debug('  @Upstream, skipping')
                    continue
                elif vid in vid_variables:
                    # logger.debug('  @Container Variables, skipping')
                    continue
                swidgets[name] = widget
                wvariables[vid] = widget.variable
                vwidgets[vid].append(name)
            elif isinstance(widget, ContainerWidget):
                # logger.debug('| Container: @%s', name)
                cwidgets[name] = widget
        vid_upstream.update(wvariables, vid_variables)
        # logger.debug('%r STOP', self)
        return ContainerState(swidgets, cwidgets, self._variables, wvariables, dict(vwidgets),
                              vid_upstream=vid_upstream)

    def setup_state(self, **kwargs):
        # Default State:
        # - All the attached variables
        # - All the shared variables
        # - All the single-variable widgets
        # - The container widgets, taking the existing variables into account
        container_state = self.state_c(**kwargs)
        rvalue: typing.Mapping[str, model.WidgetDynamicState] = {}
        wids_done = []
        for vn, v in container_state.variables.items():
            rvalue[vn] = model.WidgetDynamicState(v.get, v.set, noneable=False)
        for v, ws in container_state.vwidgets.items():
            if v is not None and len(ws) > 1:
                wv = container_state.wvariables[v]
                assert v not in rvalue, f'{self!r}: Aliased vwidgets "{v}"'
                rvalue[v] = model.WidgetDynamicState(wv.get, wv.set, noneable=False)
                wids_done.extend(ws)
        for n, w in container_state.swidgets.items():
            if n not in wids_done:
                assert n not in rvalue, f'{self!r}: Aliased swidgets "{n}"'
                rvalue[n] = model.WidgetDynamicState(
                    w.wstate_get,
                    w.wstate_set,
                    noneable=w.isNoneable,
                )
        vid_upstream = container_state.vid_upstream
        for n, wc in container_state.cwidgets.items():
            assert n not in rvalue, f'{self!r}: Aliased cwidgets "{n}"'
            rvalue[n] = model.WidgetDynamicState(
                partial(wc.state_get, vid_upstream=vid_upstream),
                partial(wc.state_set, vid_upstream=vid_upstream),
                noneable=wc.isNoneable,
                container=True,  # Propagate container data
            )
        return rvalue

    def setup_layout(self, layout: typing.Optional[str]) -> None:
        '''Useful for manual adjustments to the automatic layout.

        Args:
            layout: This is the string passed to the upstream function.

        Note:
            Available for subclass redefinition.
        '''
        pass

    def set_gui_substate(self, state: typing.Optional[model.GuiState] = None, **kwargs) -> None:
        '''Set GUI State for all sub-widgets.

        See Also:
            `MixinWidget.gstate`: Property changed for all sub-widgets.
        '''
        if state is None:
            state = model.GuiState(**kwargs)
        for _, subwidget in self.widgets.items():
            subwidget.gstate = state

    def setup_defaults(self) -> None:
        '''Runs after the widget is completely setup.

        Note this runs before the parent widget is complete ready.

        Useful to set default values.

        Note:
            Available for subclass redefinition.

        See Also:
            `setup_adefaults`: Run code after all widgets are stable (including
            parent widgets in the tree).
        '''
        pass

    def setup_adefaults(self) -> None:
        '''Runs after all widgets are stable.

        Avoid changing state on this function.

        Note:
            Available for subclass redefinition.

        See Also:
            `setup_defaults`: Run code right after this widget is setup, before
            all widgets are stable.
        '''
        pass

    def wimage(self, key: str) -> typing.Optional[tk.Image]:
        '''Wraper for `RootWindow.wimage`.'''
        return self.wroot.wimage(key)
