""" Common names for perf files. """
SIZES = [2**i for i in range(1, 25)]

IMPORT = """
from bit import BIT
from operator import add, sub
"""
IMPORT_INIT = "\n".join([IMPORT, "b = BIT(range({0}), add, sub)"])

__all__ = ['SIZES', 'IMPORT', 'IMPORT_INIT']
