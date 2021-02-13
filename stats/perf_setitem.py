""" Perf for setitem on BIT structure, should show O(logn). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_setitem():
    """ todo: worse spot to setitem? """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="b[0] = {0}".format(size-1),
            setup=IMPORT_INIT.format(size)
        )


if __name__ == "__main__":
    perf_setitem()
