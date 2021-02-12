""" Perf for creating the BIT structure, should show O(N). """
from common import sizes
import pyperf


setup = """
from bit import BIT
from operator import add, sub
"""


def perf_create():
    runner = pyperf.Runner()
    for size in sizes:
        runner.timeit(
            "{0}".format(size),
            stmt="BIT(range({0}), add, sub)".format(size),
            setup=setup
        )


if __name__ == "__main__":
    perf_create()
