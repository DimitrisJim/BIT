""" Perf for creating the BIT structure, should show O(N). """
from common import SIZES, IMPORT
import pyperf


def perf_create():
    """ Basically testing bit_layout. """
    runner = pyperf.Runner()
    for size in SIZES:
        runner.timeit(
            "{0}".format(size),
            stmt="BIT(range({0}), add, sub)".format(size),
            setup=IMPORT
        )


if __name__ == "__main__":
    perf_create()
