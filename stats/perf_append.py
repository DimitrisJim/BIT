""" Perf file for append operations, should show O(logN). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_append():
    """ todo: Append only to even length, right? """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="b.append(0)",
            setup=IMPORT_INIT.format(size - 1),
        )


if __name__ == "__main__":
    perf_append()
