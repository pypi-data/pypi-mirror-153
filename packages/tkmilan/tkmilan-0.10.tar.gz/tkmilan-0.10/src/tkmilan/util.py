'''Utility functions.'''
import math
import tkinter as tk


TK_VERSION = tuple(int(n) for n in str(tk.TkVersion).split('.'))
'''
Get the tk version as an integer tuple.

Similar to `sys.version_info`.
'''


def lcm_multiple(*numbers):
    '''
    Least Common Multiple: Multiple number

    .. note::

        Python 3.9 has `math.lcm <https://docs.python.org/3.9/library/math.html?highlight=math%20lcm#math.lcm>`_.
    '''
    if len(numbers) > 0:
        lcm = numbers[0]
        for n in numbers[1:]:
            lcm = lcm_single(lcm, n)
        return lcm
    else:
        return None


def lcm_single(a, b):
    '''
    Least Common Multiple: Single Pair
    '''
    if a == 0 and b == 0:
        return 0
    else:
        return int((a * b) / math.gcd(a, b))
