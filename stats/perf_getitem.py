""" Perf for __getitem__ on BIT structure. Should show O(logn). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_getitem():
    """ todo: worse place to index? """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="b[{0}]".format(size-1),
                setup=IMPORT_INIT.format(size)
        )


if __name__ == "__main__":
    perf_getitem()
