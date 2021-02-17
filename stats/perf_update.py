""" Perf for update on BIT structure, should show O(logn). """
from common import SIZES, IMPORT_INIT
import pyperf


def perf_update():
    """ Worse position to place new index is 0. This triggers
    a re-adjustment of the most consequent values.
    (see _follow_left in BIT for why.)
    """
    runner = pyperf.Runner()
    for size in SIZES:
        size = size + 1
        runner.timeit(
            "{0}".format(size),
            stmt="b.update(0, 0)",
            setup=IMPORT_INIT.format(size)
        )


if __name__ == "__main__":
    perf_update()
