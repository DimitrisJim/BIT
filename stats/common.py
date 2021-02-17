""" Common names for perf files. """

# Sizes to be built.
SIZES = [2**i for i in range(1, 20)]

# IMPORT just imports needed objects.
# IMPORT_INIT also initializes a BIT.
IMPORT = """
from bit import BIT
from operator import add, sub
"""
IMPORT_INIT = "\n".join([IMPORT, "b = BIT(range({0}), add, sub)"])
# Relative to top level.
RESULTS_PATH = 'stats/results/'

__all__ = ['SIZES', 'IMPORT', 'IMPORT_INIT', 'RESULTS_PATH']
