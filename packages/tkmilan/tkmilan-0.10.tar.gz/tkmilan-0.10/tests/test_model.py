import typing
import unittest
import logging

from defaultlist import defaultlist

from tkmilan.model import Direction

logger = logging.getLogger(__name__)


class Test_Direction_Grid(unittest.TestCase):
    GOLDEN = {
        ((1, 2), None): {
            Direction.N: ((0, 1),),
            Direction.S: ((0, 1),),
            Direction.E: ((0, 1),),
            Direction.W: ((1, 0),),
        },
        ((2, 1), None): {
            Direction.N: ((1,), (0,)),
            Direction.S: ((0,), (1,)),
            Direction.E: ((0,), (1,)),
            Direction.W: ((0,), (1,)),
        },
        ((2, 2), None): {
            Direction.N: ((1, 3), (0, 2)),
            Direction.S: ((0, 2), (1, 3)),
            Direction.E: ((0, 1), (2, 3)),
            Direction.W: ((1, 0), (3, 2)),
        },
        ((3, 3), None): {
            Direction.N: ((2, 5, 8), (1, 4, 7), (0, 3, 6)),
            Direction.S: ((0, 3, 6), (1, 4, 7), (2, 5, 8)),
            Direction.E: ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
            Direction.W: ((2, 1, 0), (5, 4, 3), (8, 7, 6)),
        },
        # With amounts
        ((2, 2), 3): {
            Direction.N: ((1, 2), (0, 2)),
            Direction.S: ((0, 2), (1, 2)),
            Direction.E: ((0, 1), (2, 2)),
            Direction.W: ((1, 0), (2, 2)),
        },
        ((3, 3), 7): {
            Direction.N: ((2, 5, 6), (1, 4, 6), (0, 3, 6)),
            Direction.S: ((0, 3, 6), (1, 4, 6), (2, 5, 6)),
            Direction.E: ((0, 1, 2), (3, 4, 5), (6, 6, 6)),
            Direction.W: ((2, 1, 0), (5, 4, 3), (6, 6, 6)),
        },
    }
    ROTTEN = (  # Direction, *args, amount
        # Empty Columns
        (Direction.N, (2, 5), 7),
        (Direction.S, (2, 5), 7),
        # Empty Rows
        (Direction.E, (5, 2), 7),
        (Direction.W, (5, 2), 7),
    )

    def runTest(self):
        logger.info(f'Testing "{self.__class__.__name__}"')
        for ((r, c), amount), golden in self.GOLDEN.items():
            for d in Direction:
                with self.subTest(r=r, c=c, amount=amount, d=d):
                    matrix: typing.List[typing.List[typing.Optional[int]]] = [[None for _ in range(c)] for _ in range(r)]
                    for idx, gc in enumerate(d.grid(r, c, amount=amount)):
                        for dr in range(gc.rowspan):
                            for dc in range(gc.columnspan):
                                matrix[gc.row + dr][gc.column + dc] = idx
                    logger.info('» %dx%d%s %s', r, c, '[%d]' % amount if amount else '', d.name)
                    for row in matrix:
                        logger.info('| %s', ' '.join(('x' * 2 if i is None else '%02d' % i for i in row)))
                    matrix_tuple = tuple(map(tuple, matrix))
                    if d not in golden:
                        self.fail('Missing @ %dx%d: `Direction.%s: %r,`' % (r, c, d.name, matrix_tuple))
                    self.assertEqual(golden[d], matrix_tuple, 'Error when calculation coordinates')
        for (d, (r, c), amount) in self.ROTTEN:
            with self.subTest(r=r, c=c, amount=amount, d=d):
                with self.assertRaises(ValueError) as e:
                    list(d.grid(r, c, amount=amount))
                logger.info('» %dx%d%s %s', r, c, '[%d]' % amount if amount else '', d.name)
                logger.info('  %s', e.exception)


class Test_Direction_Multiple(unittest.TestCase):
    GOLDEN = {
        ((1, 3), None): {
            Direction.N: ((0, 3), (0, 2), (0, 1)),
            Direction.S: ((0, 1), (0, 2), (0, 3)),
            Direction.E: ((0, 0, 0), (1, 2, 3)),
            Direction.W: ((0, 0, 0), (3, 2, 1)),
        },
        ((2, None, 2), 7): {
            Direction.N: ((1, 4, 6), (1, 4, 6), (1, 3, 6), (0, 3, 5), (0, 2, 5), (0, 2, 5)),
            Direction.S: ((0, 2, 5), (0, 2, 5), (0, 3, 5), (1, 3, 6), (1, 4, 6), (1, 4, 6)),
            Direction.E: ((0, 0, 0, 1, 1, 1), (2, 2, 3, 3, 4, 4), (5, 5, 5, 6, 6, 6)),
            Direction.W: ((1, 1, 1, 0, 0, 0), (4, 4, 3, 3, 2, 2), (6, 6, 6, 5, 5, 5)),
        },
    }
    ROTTEN = (  # Direction, amounts, amount
        # Non-Integer amount to distribute
        (None, (None, None), 3),
        (None, (None, 1, None), 4),
    )

    def runTest(self):
        logger.info(f'Testing "{self.__class__.__name__}"')
        for (amounts, amount), golden in self.GOLDEN.items():
            for d in Direction:
                with self.subTest(d=d, amounts=amounts):
                    matrix = defaultlist(lambda: defaultlist())
                    for idx, gc in enumerate(d.multiples(*amounts, amount=amount)):
                        for dr in range(gc.rowspan):
                            for dc in range(gc.columnspan):
                                matrix[gc.row + dr][gc.column + dc] = idx
                    logger.info('» %s (%s)%s', d.name, ' '.join((str(a) if a else 'x' for a in amounts)), '[%d]' % amount if amount else '')
                    for row in matrix:
                        logger.info('| %s', ' '.join(('x' * 2 if i is None else '%02d' % i for i in row)))
                    matrix_tuple = tuple(map(tuple, matrix))
                    if d not in golden:
                        self.fail('Missing @ %s: `Direction.%s: %r,`' % ((amounts, amount), d.name, matrix_tuple))
                    self.assertEqual(golden[d], matrix_tuple, 'Error when calculation coordinates')
        for (ds, amounts, amount) in self.ROTTEN:
            for d in Direction if ds is None else (ds,):
                with self.subTest(d=d, amounts=amounts):
                    with self.assertRaises(ValueError) as e:
                        list(d.multiples(*amounts, amount=amount))
                    logger.info('» %s (%s)%s', d.name, ' '.join((str(a) if a else 'x' for a in amounts)), '[%d]' % amount if amount else '')
                    logger.info('  %s', e.exception)


if __name__ == '__main__':
    import sys
    logs_lvl = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=logs_lvl, format='%(levelname)5.5s:%(funcName)s: %(message)s', stream=sys.stderr)
    unittest.main()
