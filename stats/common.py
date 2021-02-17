""" Common names for perf files. """

# Sizes to be built.
SIZES = [2 ** i for i in range(1, 22)]
OPS = [
    # -- O(N) --
    'create',   # plot ok, easy O(N)
    'layout',   # plot ok, easy O(N)
    # -- O(logN) --
    'append',   # plot ok, logN
    'getitem',  # plot ok, logN.
    'setitem',  # plot ok, logN
    'update',   # plot ok, logN.
]
# IMPORT just imports needed objects.
# IMPORT_INIT also initializes a BIT.
IMPORT = """
from bit import BIT
from operator import add, sub
"""
IMPORT_INIT = "\n".join([IMPORT, "b = BIT(range({0}), add, sub)"])
# Relative to top level.
RESULTS_PATH = 'stats/results/'
PLOTS_PATH = 'stats/plots/'
RES_FMT = f"{RESULTS_PATH}{{0}}.json"

__all__ = [
    'SIZES', 'OPS', 'IMPORT',
    'IMPORT_INIT', 'RESULTS_PATH',
    'RES_FMT', 'PLOTS_PATH'
]
