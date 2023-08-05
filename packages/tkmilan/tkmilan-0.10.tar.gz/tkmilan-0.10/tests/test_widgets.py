# import typing
import unittest
import logging

from tkmilan import autolayout
from tkmilan.model import GridCoordinates as GC

logger = logging.getLogger(__name__)


class Test_autolayout(unittest.TestCase):
    SINGLE = [
        autolayout.AUTO,
        autolayout.HORIZONTAL,
        autolayout.VERTICAL,
        'X', 'xN', 'xS',
        'R1', 'r1',
        'C1', 'c1',
    ]

    MULTIPLE = [
        ('xE', [  # Square, grow right
            GC(0, 0), GC(0, 1), GC(1, 0), GC(1, 1),
        ]),
        ('xW', [  # Square, grow left
            GC(0, 1), GC(0, 0), GC(1, 1), GC(1, 0),
        ]),
        ('xS', [  # Square minus 1, grow down
            GC(0, 0), GC(1, 0),
            GC(0, 1, rowspan=2),
        ]),
    ]

    def setUp(self):
        # "Beautify" the GridCoordinates `repr`
        GC.__repr__ = GC.__str__

    def test_singlewidget(self):
        logger.debug('Testing single widgets...')
        for layout in self.SINGLE:
            with self.subTest(layout=layout):
                self.assertEqual(list(autolayout.do(layout, 1)[1]), [
                    GC(0, 0),
                ])

    def test_multiplewidgets(self):
        logger.debug('Testing multiple widgets...')
        for layout, result in self.MULTIPLE:
            amount = len(result)
            with self.subTest(layout=layout, amount=amount):
                self.assertEqual(list(autolayout.do(layout, amount)[1]), result)


if __name__ == '__main__':
    import sys
    logs_lvl = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=logs_lvl, format='%(levelname)5.5s:%(funcName)s: %(message)s', stream=sys.stderr)
    unittest.main()
