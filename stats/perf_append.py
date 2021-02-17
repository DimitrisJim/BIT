""" Perf file for append operations, should show O(logN). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_append():
    """ Silly mistake: calling just a bare append appends endlessly
    thereby averaging out true cost of worse case append. 

    As such, we immediately pop after appending, this is O(1) for
    popping of the end (a constant factor for each call) and
    allows us to always check worse case append.

    Worse case append: append will result in length of BIT
    being a power of 2.
    """
    runner = pyperf.Runner()
    for size in SIZES:
        size = size - 1
        runner.timeit(
            "{0}".format(size),
            stmt="b.append(0); b.pop()",
            setup=IMPORT_INIT.format(size),
        )


if __name__ == "__main__":
    perf_append()
