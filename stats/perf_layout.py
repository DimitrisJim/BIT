""" Perf file for translating to original layout. Should show O(N). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_olayout():
    """ Continuously append to Binary indexed tree.
    Use size - 1 in order to get worse case.
    """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="b.original_layout()",
            setup=IMPORT_INIT.format(size)
        )


if __name__ == "__main__":
    perf_olayout()
