'''
Auto Layout capabilities.
'''
import logging
import warnings
import typing
import math

import tkinter as tk

from . import model

logger = logging.getLogger(__name__)

# Automatic Layout
# - HORIZONTAL
# - VERTICAL
AUTO: str = 'auto'
HORIZONTAL = tk.HORIZONTAL
VERTICAL = tk.VERTICAL

LAYOUT_SYNONYMS: typing.Mapping[str, str] = {
    HORIZONTAL: '1x',  # 1 Row
    VERTICAL: 'x1',  # 1 Column
    AUTO: 'x',  # Square
}
# Multiples
# - Use the direction names directly? With a prefix?
LAYOUT_MULTIPLE: typing.Mapping[str, model.Direction] = {
    'R': model.Direction.E,
    'r': model.Direction.W,
    'C': model.Direction.S,
    'c': model.Direction.N,
}


def do(layout_input: typing.Optional[str], amount: int) -> typing.Tuple[typing.Optional[str], typing.Iterable[model.GridCoordinates]]:
    # Pre-Process
    layout = None
    args: typing.Iterable[model.GridCoordinates] = iter([])
    if layout_input:
        layout = LAYOUT_SYNONYMS.get(layout_input, layout_input)
        assert layout is not None, f'Invalid Layout: {layout_input}'
    if __debug__:
        logger.debug(f'Final Layout: {layout}')
    # Do it!
    if layout:
        direction_names = tuple(d.name for d in model.Direction)
        try:
            if layout.startswith(('x', 'X')):
                auto_separator = layout[0]
                if layout[1:] in ('', *direction_names):
                    square = math.ceil(math.sqrt(amount))
                    logger.debug('Layout: Square (%d)', square)
                    layout = layout.replace(auto_separator, '%d%s%d' % (square, auto_separator, square), 1)
                    logger.debug('      : %s', layout)
            if layout.startswith(tuple(LAYOUT_MULTIPLE)):
                _type = layout[0]
                multiple_direction = LAYOUT_MULTIPLE[_type]
                logger.debug('Layout: Multiples %s: %s', _type, multiple_direction)

                def parse_amount(value):
                    # Allow 'x' to be replaced with the remaining widgets
                    if value == 'x':
                        return None
                    else:
                        int_value = int(value)
                        if int_value == 0:
                            raise ValueError('Layout Multiples: Invalid Value: %s' % value)
                        return int_value
                amounts = [parse_amount(v) for v in layout[1:].split(',')]
                args = multiple_direction.multiples(*amounts, amount=amount)
            elif 'x' in layout or 'X' in layout:
                auto_direction = model.Direction.S  # Default automatic Direction
                if any(layout.endswith(name) for name in direction_names):
                    # Requires the Direction name to be 1 character long
                    auto_direction = model.Direction[layout[-1]]
                    layout = layout[:-1]
                auto_force: bool = 'X' in layout
                assert isinstance(auto_direction, model.Direction)
                if auto_force:
                    auto_separator = 'X'
                    assert 'x' not in layout
                else:
                    auto_separator = 'x'
                    assert 'X' not in layout
                rows, cols = [None if v == '' else int(v) for v in layout.split(auto_separator)]
                # At least one of `rows`/`cols` is not `None`
                if rows is None:
                    assert cols is not None
                    rows = math.ceil(amount / cols)
                if cols is None:
                    assert rows is not None
                    cols = math.ceil(amount / rows)
                grid_missing = rows * cols - amount
                if grid_missing > 0 and not auto_force:
                    if grid_missing >= cols:
                        dcols = grid_missing // cols
                        logger.debug('      : -%d Columns', dcols)
                        cols -= dcols
                        grid_missing = rows * cols - amount
                        if __debug__:
                            if layout_input not in LAYOUT_SYNONYMS:
                                # This might be a spurious warning
                                warnings.warn('Non-automatic layout being unsquared: %d cols' % dcols, stacklevel=4)
                    if grid_missing >= rows:
                        drows = grid_missing // rows
                        logger.debug('      : -%d Rows', drows)
                        rows -= drows
                        grid_missing = rows * cols - amount
                        if __debug__:
                            if layout_input not in LAYOUT_SYNONYMS:
                                # This might be a spurious warning
                                warnings.warn('Non-automatic layout being unsquared: %d rows' % drows, stacklevel=4)
                logger.debug('Layout: Automatic Grid (%d%s%d%s)[%+d]', rows, auto_separator, cols, auto_direction.name, grid_missing)
                args = auto_direction.grid(rows, cols, amount=amount,
                                           auto_fill=not auto_force)
            container_matrix = None  # For debug
            if __debug__:
                try:
                    from defaultlist import defaultlist  # type: ignore
                    container_matrix = defaultlist(lambda: defaultlist())
                except ImportError:
                    pass  # Don't use if it doesn't exist
                logged_args = []  # Consume the iterator for logging ...
                for idx, arg in enumerate(args):
                    logged_args.append(arg)
                    if container_matrix is not None:
                        for drow in range(arg.rowspan):
                            for dcol in range(arg.columnspan):
                                container_matrix[arg.row + drow][arg.column + dcol] = idx
                    else:
                        logger.debug('| %s' % arg)
                if container_matrix is not None:
                    for r in container_matrix:
                        assert isinstance(r, typing.Sequence)
                        logger.debug('| %s', ' '.join(('x' * 2 if i is None else '%02d' % i for i in r)))
                args = iter(logged_args)  # ... and return a new iterator
        except Exception:
            args = []
    return layout, args
