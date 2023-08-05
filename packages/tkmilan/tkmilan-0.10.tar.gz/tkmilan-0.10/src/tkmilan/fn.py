'''
Functions to manipulate widgets and other objects, that make no sense to be
used externally.

If useful, they should be exposed as methods.
'''
import logging
import typing
import sys
import math
from functools import wraps
from textwrap import dedent
from pathlib import Path

import tkinter as tk  # Only for typechecking and asserts
import tkinter.filedialog
import tkinter.messagebox

from . import model
if typing.TYPE_CHECKING:
    from . import mixin


logger = logging.getLogger(__name__)


# TODO: Localisation? Get the localised values from tk?
gettext_ALL_FILES = 'All Files'
gettext_SUPPORTED_FILES = 'All Supported Filetypes'
gettext_LOAD = 'Load'
gettext_OPEN = 'Open'
gettext_SAVE = 'Save'


def label_size(chars: int) -> int:
    '''Estimate a label size (in pixels) by counting the number of chars.'''
    # TODO: Measure the font size: https://stackoverflow.com/a/30952406
    return math.ceil(-4 + 6 * math.pow(chars, 0.41))


def grid_size(*widgets: 'mixin.MixinWidget') -> 'model.GridSize':
    """Get the grid size for the given widgets.

    This should be used by a frame to calculate its grid size,
    by checking the values for all its children widgets.

    Args:
        widgets: Widgets in the same grid. There should be at least one.
    """
    def maxs(w: 'mixin.MixinWidget') -> typing.Tuple[int, int]:
        info = w.wgrid
        # logger.debug(f'=> Grid Info: {info}')
        if info is None:
            return (-1, -1)  # Not included on a grid yet
        else:
            return (info.row + info.rowspan - 1, info.column + info.columnspan - 1)
    if __debug__:
        parents = set()
        for w in widgets:
            if w.wparent:
                parents.add(w.wparent)
        assert len(parents) == 1, f'Grid Size only for sibling widgets. Parents: {parents}'
    m = [maxs(w) for w in widgets]
    num_columns = max([w[1] for w in m]) + 1
    num_rows = max([w[0] for w in m]) + 1
    return model.GridSize(rows=num_rows, columns=num_columns)


def configure_grid(master: 'mixin.ContainerWidget',
                   column_weights: typing.Sequence[int], row_weights: typing.Sequence[int],
                   **kwargs: typing.Mapping[str, typing.Any]) -> None:
    """Configure the grid.

    Weights can be:

        - ``0`` : Fit the widgets, never resize
        - ``>0``: Resize with this number as weight

    Make sure to include all columns and rows. When in doubt, use 0.

    Args:
        column_weights: List of column weights
        row_weights: List of row weights
        kwargs: Extra arguments to the configuration functions
            `columnconfigure <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M8>`_
            /
            `rowconfigure <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M24>`_.
    """
    if __debug__:
        gw = master.gsize
        gr = model.GridSize(rows=len(row_weights), columns=len(column_weights))
        assert gw == gr, f'{master!r}: Invalid grid size: W::{gw} R::{gr}'
    assert isinstance(master, (tk.Widget, tk.Tk)), f'{master} is not a valid tkinter.Widget'
    for col, w in enumerate(column_weights):
        master.columnconfigure(col, weight=w, **kwargs)  # type: ignore  # Invalid Types
    for row, h in enumerate(row_weights):
        master.rowconfigure(row, weight=h, **kwargs)  # type: ignore  # Invalid Types


def configure(master: 'mixin.ContainerWidget',
              *widgets: 'mixin.MixinWidget',
              c_rows: bool = False, c_cols: bool = False,
              **kwargs: typing.Mapping[str, typing.Any]) -> None:
    '''Configure the rows and columns for the given widgets.

    For widgets that span more than one row or column, the settings are changed
    for all rows or columns.

    Args:
        widgets: Widgets to consider.
        c_rows: Configure the rows
        c_cols: Configure the columns
        kwargs: Arguments passed to the configuration functions:
            `columnconfigure <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M8>`_
            /
            `rowconfigure <https://www.tcl.tk/man/tcl/TkCmd/grid.html#M24>`_.
    '''
    assert isinstance(master, (tk.Widget, tk.Tk)), f'{master} is not a valid tkinter.Widget'
    for w in widgets:
        wgrid = w.wgrid
        if wgrid and c_rows:
            for r in range(wgrid.row, wgrid.row + wgrid.rowspan):
                master.rowconfigure(r, **kwargs)  # type: ignore  # Invalid Types
        if wgrid and c_cols:
            for c in range(wgrid.column, wgrid.column + wgrid.columnspan):
                master.columnconfigure(c, **kwargs)  # type: ignore  # Invalid Types


def generate_trace(variable: tk.Variable, function: typing.Callable, **kwargs):
    '''Generate an internal trace callback.

    The function generated here should be attached to the ``Tk`` event.
    '''
    @wraps(function)
    def wrapper(name: str, index: typing.Any, etype: model.TraceModeT):  # "Real" tk function
        assert isinstance(name, str) and isinstance(etype, str)
        return function(variable, etype, **kwargs)
    return wrapper


def vname(variable: tk.Variable) -> str:
    '''Collect the variable name.

    This is set on the object, but there's no typing support for it. Double check it here.
    '''
    assert hasattr(variable, '_name'), 'tk.Variable has changed the implementation'
    return variable._name  # type: ignore


def bind_mousewheel(widget, up: typing.Callable, down: typing.Callable, **kwargs) -> typing.Union[model.Binding, typing.Tuple[model.Binding, model.Binding]]:
    '''OS-independent mouse wheel bindings.

    This is a digital scroll.

    On Linux, this is implemented as two special mouse buttons ("up" and
    "down". Windows supports analog mouse wheels, but this function emulates a
    digital scroll out of that.

    The return value is platform-specific:

    - On Linux, return the two `Binding` object, for "up" and "down" mouse
      scroll.

    - On Windows, returns the single `Binding` object for the analog mouse
      scroll.

    Note:
        This uses regular `Binding` objects, remember that ``immediate=True``
        is needed to activate the binding on start.
    '''
    if sys.platform == 'linux':
        bup = model.Binding(widget, '<Button-4>', up, **kwargs)
        bdown = model.Binding(widget, '<Button-5>', down, **kwargs)
        return bup, bdown
    elif sys.platform == 'win32':
        def wrap_scroll(event):
            if event.delta > 0:
                return up(event)
            elif event.delta < 0:
                return down(event)
            else:
                raise NotImplementedError
        binding = model.Binding(widget, '<MouseWheel>', wrap_scroll, **kwargs)
        return binding
    else:
        logger.critical(f'Unsupported system platform: {sys.platform}')
        return NotImplementedError


def _filedialog_fts(filetypes, includeSupported, includeAll):
    ''''''  # Internal, do not document
    fts = [(t, ft.pattern) for t, ft in filetypes.items()]
    if includeSupported is True and len(fts) > 1:
        fts.insert(0, (gettext_SUPPORTED_FILES, tuple([s for _, s in fts])))
    if includeAll:
        fts.append((gettext_ALL_FILES, '*'))
    return fts


def _filedialog_directory(initialDirectory: typing.Optional[Path], **kwargs: typing.Any) -> typing.Optional[Path]:
    ''''''  # Internal, do not document
    if initialDirectory:
        kwargs['initialdir'] = str(initialDirectory)
    rvalue = tk.filedialog.askdirectory(**kwargs)
    if rvalue is None or rvalue in ((), ''):  # Support multiple Python/Tk versions
        return None
    else:
        return Path(rvalue)


# TODO: Sub-class `tkinter.filedialog.FileDialog`, to implement the `askretrycancel` part?
def _filedialog_file(fn: typing.Callable, initialDirectory: typing.Optional[Path], filetypes: model.FileTypes, real_title: str, includeSupported: bool, includeAll: bool, configureDefault: bool, **kwargs: typing.Any) -> typing.Optional[Path]:
    ''''''  # Internal, do not document
    if initialDirectory:
        kwargs['initialdir'] = str(initialDirectory)
    # Default Extension
    if len(filetypes) > 0 and configureDefault:
        # TODO: configureDefault can be an index into `filetypes.values()`
        defaultPattern = list(filetypes.values())[0]
        defaultextension = defaultPattern.suffix
    else:
        defaultextension = ''
    kwargs.update({
        'filetypes': _filedialog_fts(filetypes, includeSupported, includeAll),
        'defaultextension': defaultextension,
    })
    label_ftypes = [f'- {lbl}: {ft.pattern}' for lbl, ft in filetypes.items()]
    ask: bool = True  # Should we ask again?
    rvalue = None
    while ask:
        rvalue = fn(**kwargs)
        if rvalue is None or rvalue in ((), ''):  # Support multiple Python/Tk versions
            # User clicked cancel, bail with `None`
            ask, rvalue = False, None
        else:
            rvalue = Path(rvalue)
            if includeAll:
                # Accept all file names, independent of filetypes
                ask = False
            else:
                # Accept only the given FileTypes
                ask = not any(ft.matches(rvalue) for ft in filetypes.values())
        if ask:
            # Again! Ask the user for another file (or allow it to leave)
            label = dedent('''
            Invalid File:
            %s
            Allowed File Types:
            %s
            ''').strip() % (rvalue, '\n'.join(label_ftypes))
            if not tk.messagebox.askretrycancel(title=real_title, message=label):
                ask, rvalue = False, None
    return rvalue


def ask_directory_load(parent: 'mixin.MixinWidget',
                       title: str = 'Folder', full_title: typing.Optional[str] = None,
                       initialDirectory: typing.Optional[Path] = None,
                       **kwargs) -> typing.Optional[Path]:
    '''Wrap a file dialog that returns a directory name, for loading data.

    ..
        Python 3.8 is missing this reference, included in Python 3.9:

        See Python documentation in `tkinter.filedialog.askdirectory`.

    Since this is for loading data, it will guarantee the directory exists.

    Args:
        title: Window Title, prefixed by the operation mode.
        full_title: Override final ``title``, ignoring the operation mode.
            Optional.
        initialDirectory: Initial Directory to open the dialog, or `None` to use the
            OS-specific default.

            Optional, defaults to `None`.
        kwargs: Passed to the upstream function.

    Returns:
        If the user bails, return `None`.
        Otherwise return a `Path <pathlib.Path>`, guaranteed to be a directory.

    See Also:
        See `ask_directory_save` for the Save alternative to this function.
    '''
    kwargs.update({
        'parent': parent,
        'title': full_title or f'{gettext_LOAD} {title}',
        'mustexist': True,
    })
    path = _filedialog_directory(initialDirectory, **kwargs)
    if __debug__:
        # `mustexist` already guarantees this, just double checking on debug mode
        if path is not None:
            assert path.is_dir(), f'Invalid directory: {path!r}'
    return path


def ask_directory_save(parent: 'mixin.MixinWidget',
                       title: str = 'Folder', full_title: typing.Optional[str] = None,
                       initialDirectory: typing.Optional[Path] = None,
                       **kwargs) -> typing.Optional[Path]:
    '''Wrap a file dialog that returns a directory name, for saving data.

    ..
        Python 3.8 is missing this reference, included in Python 3.9:

        See Python documentation in `tkinter.filedialog.askdirectory`.

    Since this is for saving data, it allows for non-existing directories.

    Args:
        title: Window Title, prefixed by the operation mode.
        full_title: Override final ``title``, ignoring the operation mode.
            Optional.
        initialDirectory: Initial Directory to open the dialog, or `None` to use the
            OS-specific default.

            Optional, defaults to `None`.
        kwargs: Passed to the upstream function.

    Returns:
        If the user bails, return `None`.
        Otherwise return a `Path <pathlib.Path>`.

    See Also:
        See `ask_directory_load` for the Load alternative to this function.
    '''
    kwargs.update({
        'parent': parent,
        'title': full_title or f'{gettext_SAVE} {title}',
        'mustexist': False,
    })
    return _filedialog_directory(initialDirectory, **kwargs)


def ask_file_load(parent: 'mixin.MixinWidget',
                  title: str = 'File', full_title: typing.Optional[str] = None,
                  initialDirectory: typing.Optional[Path] = None,
                  filetypes: typing.Optional[model.FileTypes] = None,
                  includeSupported: bool = True, includeAll: bool = True, configureDefault: bool = False,
                  **kwargs) -> typing.Optional[Path]:
    '''Wrap a file dialog that returns a file name, for loading data.

    ..
        Python 3.8 is missing this reference, included in Python 3.9:

        See ``Tk`` documentation in `tk.filedialog.askopenfilename`.

    Since this is for loading data, it will guarantee the file exists.

    Args:
        title: Window Title, prefixed by the operation mode.
        full_title: Override final ``title``, ignoring the operation mode.
            Optional.
        initialDirectory: Initial Directory to open the dialog, or `None` to use the
            OS-specific default.
            Optional, defaults to `None`.
        filetypes:
            `FileTypes <model.FileTypes>` object with all supported
            `FileType` patterns.

            This is a mapping from UI string, to `FileType` object.
            The default option is the first one, but this interacts with
            ``includeSupported``.

            Optional, when not given it acts as no filetypes are supported. See
            ``includeAll``.
        includeSupported:
            Include a pattern for all supported filetypes, on the filetypes list.

            This is included as the first pattern, therefor it acts as the default selection.
            Only included if there is more that one filetype.

            Defaults to `True`.
        includeAll:
            Include a pattern for all files, on the filetypes list.

            This is included as the last pattern, so it will be the default
            only if there are no supported filetypes.

            Defaults to `True`.
        configureDefault:
            Configure the default suffix as the first element on ``filetypes``
            (if exists). This is pure evil because the user will get a suffix
            added that is not shown anywhere.

            Defaults to `False`.

        kwargs: Passed to the upstream function.

    Note:
        Giving no ``filetypes`` forces ``includeAll`` to `True`.

    Returns:
        If the user bails or the selected file is not supported, return `None`.
        Otherwise return a `Path <pathlib.Path>`, guaranteed to be a file.

    See Also:
        See `ask_file_save` for the Save alternative to this function.
    '''
    # Setup the filetype argument
    if filetypes is None:
        filetypes = model.FileTypes()
        includeAll = True
    real_title = full_title or f'{gettext_LOAD} {title}'
    kwargs.update({
        'parent': parent,
        'title': real_title,
    })
    path = _filedialog_file(tk.filedialog.askopenfilename,
                            initialDirectory, filetypes, real_title, includeSupported, includeAll, configureDefault, **kwargs)
    if __debug__:
        if path is not None:
            assert path.is_file(), f'Invalid file: {path!r}'
    return path


def ask_file_save(parent: 'mixin.MixinWidget',
                  title: str = 'File', full_title: typing.Optional[str] = None,
                  initialDirectory: typing.Optional[Path] = None,
                  filetypes: typing.Optional[model.FileTypes] = None,
                  includeSupported: bool = False, includeAll: bool = False, configureDefault: bool = False,
                  **kwargs) -> typing.Optional[Path]:
    '''Wrap a file dialog that returns a file name, for saving data.

    ..
        Python 3.8 is missing this reference, included in Python 3.9:

        See ``Tk`` documentation in `tk.filedialog.askopenfilename`.

    Since this is for saving data, it allows for non-existing files.

    Args:
        title: Window Title, prefixed by the operation mode.
        full_title: Override final ``title``, ignoring the operation mode.
            Optional.
        initialDirectory: Initial Directory to open the dialog, or `None` to use the
            OS-specific default.
            Optional, defaults to `None`.
        filetypes:
            `FileTypes <model.FileTypes>` object with all supported
            `FileType` patterns.

            This is a mapping from UI string, to `FileType` object.
            The default option is the first one, but this interacts with
            ``includeSupported``.

            Optional, when not given it acts as no filetypes are supported. See
            ``includeAll``.
        includeSupported:
            Include a pattern for all supported filetypes, on the filetypes list.

            This is included as the first pattern, therefor it acts as the default selection.
            Only included if there is more that one filetype.

            Defaults to `False`.
        includeAll:
            Include a pattern for all files, on the filetypes list.

            This is included as the last pattern, so it will be the default
            only if there are no supported filetypes.

            Defaults to `False`.
        configureDefault:
            Configure the default suffix as the first element on ``filetypes``
            (if exists). This is pure evil because the user will get a suffix
            added that is not shown anywhere.

            Defaults to `False`.

        kwargs: Passed to the upstream function.

    Note:
        Giving no ``filetypes`` forces ``includeAll`` to `True`.

    Returns:
        If the user bails or the selected file is not supported, return `None`.
        Otherwise return a `Path <pathlib.Path>`.

    See Also:
        See `ask_file_load` for the Load alternative to this function.
    '''
    # Setup the filetype argument
    if filetypes is None:
        filetypes = model.FileTypes()
        includeAll = True
    real_title = full_title or f'{gettext_SAVE} {title}'
    kwargs.update({
        'parent': parent,
        'title': real_title,
    })
    return _filedialog_file(tk.filedialog.asksaveasfilename,
                            initialDirectory, filetypes, real_title, includeSupported, includeAll, configureDefault, **kwargs)


def binding_disable(event=None):
    '''Disable the binding (stop chaining the bind functions).

    Attach this function to a `Binding` event to disable the processing, even
    for further validations.
    '''
    return 'break'
